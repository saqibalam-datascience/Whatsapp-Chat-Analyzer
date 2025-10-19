import re
import pandas as pd

def preprocess(data):
    # Updated regex to handle potential variations like AM/PM, different spacing
    # Added optional seconds (:ss)? and different AM/PM casing ([ap]m|[AP]M)?
    pattern = r'(\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}(?::\d{2})?(?:\s?(?:[ap]m|[AP]M))?)\s-\s'

    # Use re.split with capturing group to keep the delimiter (date)
    parts = re.split(pattern, data)

    # The first element might be empty if the string starts with the pattern
    if not parts[0]:
        parts = parts[1:]

    # Pair dates and messages
    dates = parts[0::2] # Every even index is a date
    messages_raw = parts[1::2] # Every odd index is a message

    # Ensure equal length before creating DataFrame
    min_len = min(len(dates), len(messages_raw))
    dates = dates[:min_len]
    messages_raw = messages_raw[:min_len]

    df = pd.DataFrame({'user_message': messages_raw, 'message_date': dates})

    # --- Start of Fix ---
    # Ensure the 'message_date' column is string and strip whitespace BEFORE the loop
    if not df.empty: # Check if DataFrame is not empty
         df['message_date'] = df['message_date'].astype(str).str.strip()
    # --- End of Fix ---

    # Try different date formats
    date_formats = [
        # Note: Removed the trailing ' - ' from formats as strip() handles it
        '%d/%m/%Y, %I:%M %p', # Format with AM/PM (like 10/07/2023, 4:03 pm)
        '%d/%m/%Y, %H:%M',    # 24-hour format with 4-digit year
        '%d/%m/%y, %H:%M',    # Original format (2-digit year, 24-hour)
        '%d/%m/%y, %I:%M %p' , # 2-digit year with AM/PM
        # Add formats with seconds if needed
        '%d/%m/%Y, %I:%M:%S %p',
        '%d/%m/%Y, %H:%M:%S',
        '%d/%m/%y, %H:%M:%S',
        '%d/%m/%y, %I:%M:%S %p'
    ]

    # Apply datetime conversion, trying multiple formats
    converted_dates = pd.NaT # Initialize with Not a Time
    if not df.empty: # Check if DataFrame is not empty before proceeding
        for fmt in date_formats:
            try:
                # Attempt conversion on the original STRIPPED strings
                # Use errors='coerce' to turn unparseable dates into NaT
                # Convert the column only once after finding the best format potentially
                temp_converted = pd.to_datetime(df['message_date'], format=fmt, errors='coerce')

                # Check if this format successfully parsed more dates than previous attempts
                if converted_dates is pd.NaT or temp_converted.notna().sum() > converted_dates.notna().sum():
                     converted_dates = temp_converted

                # Optional: If a format parses almost all dates, you might break early
                # if temp_converted.notna().sum() / len(df) > 0.95:
                #     break

            except (ValueError, TypeError):
                continue # Try next format

        # Assign the best conversion result back to the DataFrame
        df['message_date'] = converted_dates


    # Drop rows where date couldn't be parsed by any format
    df.dropna(subset=['message_date'], inplace=True)

    # Rename column *after* successful conversion and dropping NaNs
    df.rename(columns={'message_date': 'date'}, inplace=True)


    users = []
    messages = []
    for message in df['user_message']:
        # Updated regex for user splitting - handles names with spaces, emojis etc. better
        # It looks for the first occurrence of ': ' AFTER the potential user name
        entry = re.split('^(.*?):\s', message, maxsplit=1)
        if len(entry) == 3:  # Successfully split into ['', user, message_content]
            users.append(entry[1])
            messages.append(entry[2])
        else: # Likely a group notification or message without ': ' separator
             # Check for common group notification patterns
             # Made patterns slightly more robust
             notification_patterns = [
                 " created group ",
                 " joined using this group's invite link",
                 " joined using a group link", # Added variation
                 " added ",
                 " changed the subject ",
                 " changed this group's icon",
                 " removed ",
                 " left", # Check if message ends with ' left'
                 " changed their phone number to a new number.",
                 " Messages and calls are end-to-end encrypted.", # Common system message
                 " changed the group description",
                 " was added",
                 " pinned a message" # Added
                 # Add other notification patterns if observed
             ]
             is_notification = False
             # Check endswith first for ' left'
             if message.strip().endswith(" left"):
                 is_notification = True
             else:
                  for pattern_text in notification_patterns:
                     if pattern_text in message:
                         is_notification = True
                         break

             if is_notification:
                 users.append('group_notification')
                 messages.append(message) # Keep the full notification text
             else:
                 # Assume it's a message from an unknown source or continuation
                 users.append('unknown_or_system') # Or you might assign the previous user if it's a multi-line msg
                 messages.append(message)


    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    # Ensure 'date' column is valid before accessing .dt properties
    if not df.empty and pd.api.types.is_datetime64_any_dtype(df['date']):
        # Ensure 'date' column is timezone-naive if it has timezone info
        if df['date'].dt.tz is not None:
             df['date'] = df['date'].dt.tz_localize(None)


        df['only_date'] = df['date'].dt.date
        df['year'] = df['date'].dt.year
        df['month_num'] = df['date'].dt.month
        df['month'] = df['date'].dt.month_name()
        df['day'] = df['date'].dt.day
        df['day_name'] = df['date'].dt.day_name()
        df['hour'] = df['date'].dt.hour
        df['minute'] = df['date'].dt.minute

        period = []
        for hour in df['hour']: # Iterate directly over the hour column
            if hour == 23:
                period.append(str(hour) + "-" + str('00'))
            elif hour == 0:
                period.append(str('00') + "-" + str(hour + 1))
            else:
                period.append(str(hour) + "-" + str(hour + 1))

        df['period'] = period
    else:
        # Handle cases where the DataFrame might be empty after cleaning, or date conversion failed entirely
        # Add necessary columns with default values if needed, or return empty df appropriately
        cols_to_add = ['only_date', 'year', 'month_num', 'month', 'day', 'day_name', 'hour', 'minute', 'period']
        for col in cols_to_add:
            if col not in df.columns:
                 df[col] = pd.NA # Or appropriate default like None, 0, ''


    return df
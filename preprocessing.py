def preprocess():
    # Renaming columns to make them easier to work with
    df.columns = [
        "timestamp", "email", "full_name", "gender", "status", "walk_run", "time", "distance", "screenshot", "photos", "anything_else"
    ]
    # Anonymize full names
    df['shortened_name'] = df['full_name'].str.split().apply(lambda x: x[0] + ' ' + x[-1][0] if len(x) > 1 else x[0])

    # Convert "time" from string to timedelta and calculate total seconds
    df['time_td'] = pd.to_timedelta(df['time'])
    df['total_seconds'] = df['time_td'].dt.total_seconds()

    # Clean 'distance' to ensure it's numeric and calculate pace
    df['distance'] = pd.to_numeric(df['distance'], errors='coerce')
    df['pace_per_mile'] = df['total_seconds'] / df['distance']
    df['formatted_pace'] = df['pace_per_mile'].apply(format_pace)

    # Unique Participants using email for internal counting
    unique_participants = df['email'].nunique()

    # Participants by Gender
    participants_by_gender = df.groupby('gender').size().reset_index(name='count')

    # Fastest Female Students
    fastest_female_students = df[(df['walk_run'] == 'I ran') & (df['gender'] == 'Female') & (df['status'].isin(['Student', 'Alumni']))].sort_values(by='total_seconds').drop_duplicates(subset=['email'], keep='first')

    # Fastest Male Students
    fastest_male_students = df[(df['walk_run'] == 'I ran') & (df['gender'] == 'Male') & (df['status'].isin(['Student', 'Alumni']))].sort_values(by='total_seconds').drop_duplicates(subset=['email'], keep='first')

    # Fastest Non-binary Students
    fastest_non_binary_students = df[(df['walk_run'] == 'I ran') & (df['gender'] == 'Non-binary') & (df['status'].isin(['Student', 'Alumni']))].sort_values(by='total_seconds').drop_duplicates(subset=['email'], keep='first')

    # Fastest Faculty/Staff
    fastest_faculty_staff = df[(df['walk_run'] == 'I ran') & (df['status'] == 'Staff/Faculty')].sort_values(by='total_seconds').drop_duplicates(subset=['email'], keep='first')

    # Runners/Walkers with at Least 15 5Ks
    runners_with_at_least_15_5ks = df.groupby('email').filter(lambda x: len(x) >= 15)

    # Most Improved Running Time (%)
    improvement_df = df[df['walk_run'] == 'I ran'].groupby('email').agg(max_pace=('total_seconds', 'max'), min_pace=('total_seconds', 'min'))
    improvement_df['improvement'] = improvement_df['max_pace'] - improvement_df['min_pace']
    improvement_df = improvement_df.sort_values(by='improvement', ascending=False)

    # Longest Walk
    longest_walk = df[df['walk_run'] == 'I walked'].sort_values(by='distance', ascending=False).head(1)

    # Median Runner/Walker
    median_time = df['total_seconds'].median()
    df['median_diff'] = (df['total_seconds'] - median_time).abs()
    median_runner = df.sort_values(by='median_diff').head(1)
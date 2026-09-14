"""
List of Bible verse references used for the daily "Verse of the Day" post.

These are REFERENCES only (e.g. "John 3:16") — the actual verse text is
fetched at post-time from the bible-api.com API. That way the text is
always accurate and you can pick any translation (see TRANSLATION in .env).

Feel free to add, remove, or edit entries. Run `python test_verses.py`
after making changes to confirm every reference resolves correctly.
"""

VERSES = [
    # Faith & Trust
    "John 3:16", "Proverbs 3:5-6", "Romans 8:28", "Hebrews 11:1",
    "Isaiah 41:10", "Joshua 1:9", "Psalm 46:1", "Psalm 56:3",
    "2 Corinthians 5:7", "Mark 9:23", "Mark 11:24", "Luke 1:37",
    "Romans 10:9", "Habakkuk 2:3", "Jeremiah 17:7-8", "Psalm 9:10",
    "Psalm 37:5", "1 Peter 5:7", "Proverbs 16:3", "Isaiah 26:3",

    # Strength & Courage
    "Philippians 4:13", "Isaiah 40:31", "2 Timothy 1:7", "Deuteronomy 31:6",
    "Deuteronomy 31:8", "Joshua 1:9", "Psalm 27:1", "Psalm 18:2",
    "Ephesians 6:10-11", "1 Chronicles 16:11", "Psalm 46:10", "Nahum 1:7",
    "Isaiah 41:13", "Psalm 138:8", "2 Chronicles 20:15", "Habakkuk 3:19",
    "Psalm 31:24", "1 Corinthians 16:13", "Zechariah 4:6",

    # Peace & Comfort
    "John 14:27", "Philippians 4:6-7", "Psalm 23:4", "Matthew 11:28-30",
    "Psalm 34:18", "Isaiah 26:3", "2 Corinthians 1:3-4", "Psalm 55:22",
    "Psalm 94:19", "Psalm 147:3", "John 16:33", "Romans 15:13",
    "Colossians 3:15", "Psalm 29:11", "Numbers 6:24-26", "Isaiah 43:2",

    # Love
    "1 Corinthians 13:4-7", "1 John 4:19", "John 15:13", "Romans 5:8",
    "1 John 4:7-8", "1 John 4:18", "John 13:34-35", "Romans 8:38-39",
    "Song of Solomon 8:7", "1 Peter 4:8", "Ephesians 5:1-2", "1 John 3:1",

    # Hope
    "Jeremiah 29:11", "Romans 15:13", "Psalm 71:14", "Lamentations 3:22-23",
    "Romans 8:24-25", "Psalm 42:11", "Isaiah 40:31", "Titus 2:13",
    "Psalm 130:5", "Hebrews 6:19", "1 Peter 1:3", "Psalm 39:7",

    # Wisdom & Guidance
    "Proverbs 3:5-6", "James 1:5", "Psalm 119:105", "Proverbs 1:7",
    "Proverbs 4:23", "Proverbs 16:9", "Proverbs 18:10", "Proverbs 27:17",
    "Isaiah 30:21", "Proverbs 19:21", "Colossians 3:23", "Ecclesiastes 3:1",
    "Proverbs 15:1", "Proverbs 22:6", "Proverbs 12:15", "James 3:17",

    # Salvation & Grace
    "Ephesians 2:8-9", "Romans 6:23", "Romans 3:23", "Romans 5:1",
    "Acts 4:12", "Acts 16:31", "2 Corinthians 5:17", "Titus 3:5",
    "John 1:12", "John 3:3", "Romans 10:13", "2 Corinthians 12:9",

    # Prayer
    "Philippians 4:6-7", "Matthew 7:7", "James 5:16", "1 Thessalonians 5:16-18",
    "Jeremiah 33:3", "John 14:13-14", "Matthew 21:22", "Ephesians 6:18",

    # Joy & Gratitude
    "Nehemiah 8:10", "Psalm 118:24", "Psalm 16:11", "1 Thessalonians 5:16-18",
    "Philippians 4:4", "Psalm 100:4-5", "James 1:2-4", "Psalm 30:5",
    "Romans 15:13", "Psalm 126:5", "Habakkuk 3:17-18",

    # Purpose & Calling
    "Jeremiah 29:11", "Ephesians 2:10", "Romans 12:2", "Esther 4:14",
    "Matthew 5:14-16", "Colossians 3:23-24", "Philippians 1:6", "1 Peter 2:9",
    "Matthew 6:33", "2 Timothy 1:9", "Galatians 2:20",

    # Perseverance
    "James 1:2-4", "Galatians 6:9", "Romans 5:3-4", "Hebrews 12:1-2",
    "2 Corinthians 4:16-18", "Philippians 3:13-14", "1 Corinthians 9:24",
    "2 Timothy 4:7", "Isaiah 40:31", "Psalm 27:14",

    # Forgiveness
    "1 John 1:9", "Colossians 3:12-14", "Ephesians 4:32", "Matthew 6:14-15",
    "Micah 7:18-19", "Psalm 103:12", "Luke 6:37",

    # God's Word
    "2 Timothy 3:16-17", "Psalm 119:105", "Hebrews 4:12", "Joshua 1:8",
    "Matthew 4:4", "Psalm 19:7-8", "Isaiah 40:8", "Psalm 1:1-3",

    # Anxiety & Worry
    "Philippians 4:6-7", "Matthew 6:34", "1 Peter 5:7", "Psalm 55:22",
    "Isaiah 41:10", "Psalm 94:19", "John 14:1", "Psalm 34:4",

    # Family & Relationships
    "Joshua 24:15", "Ephesians 6:1-4", "Proverbs 22:6", "Ruth 1:16",
    "Psalm 127:3", "Proverbs 17:17", "Colossians 3:20", "Malachi 4:6",

    # Money & Provision
    "Philippians 4:19", "Matthew 6:33", "Proverbs 3:9-10", "2 Corinthians 9:7",
    "Malachi 3:10", "1 Timothy 6:6-7", "Luke 12:34",

    # Healing & Suffering
    "Isaiah 53:5", "Psalm 34:18", "James 5:15", "Psalm 147:3",
    "2 Corinthians 12:9", "Jeremiah 30:17", "Psalm 30:2", "Exodus 15:26",

    # Identity in Christ
    "2 Corinthians 5:17", "Galatians 2:20", "Ephesians 2:10", "1 Peter 2:9",
    "Psalm 139:14", "Romans 8:1", "Galatians 3:28", "1 John 3:1",
    "John 1:12", "Colossians 3:3",

    # Creation & Nature
    "Genesis 1:1", "Psalm 19:1", "Psalm 8:3-4", "Colossians 1:16-17",
    "Psalm 24:1", "Job 12:7-10",

    # Old Testament classics
    "Genesis 50:20", "Exodus 14:14", "Leviticus 19:18", "Numbers 6:24-26",
    "Deuteronomy 6:5", "Joshua 1:9", "Judges 6:12", "Ruth 1:16",
    "1 Samuel 16:7", "1 Samuel 17:47", "2 Samuel 22:31", "1 Kings 8:57",
    "2 Kings 6:16", "1 Chronicles 16:11", "2 Chronicles 7:14",
    "Nehemiah 8:10", "Esther 4:14", "Job 19:25",

    # Psalms & Proverbs favorites
    "Psalm 8:3-4", "Psalm 16:11", "Psalm 19:14", "Psalm 23:1",
    "Psalm 27:14", "Psalm 32:8", "Psalm 34:8", "Psalm 37:4",
    "Psalm 42:1", "Psalm 46:1", "Psalm 51:10", "Psalm 62:1-2",
    "Psalm 68:19", "Psalm 73:26", "Psalm 84:11", "Psalm 86:15",
    "Psalm 90:12", "Psalm 91:1-2", "Psalm 103:1-5", "Psalm 107:1",
    "Psalm 111:10", "Psalm 112:1", "Psalm 118:24", "Psalm 119:105",
    "Psalm 121:1-2", "Psalm 121:7-8", "Psalm 133:1", "Psalm 139:14",
    "Psalm 143:8", "Psalm 145:18", "Psalm 150:6",
    "Proverbs 10:12", "Proverbs 11:25", "Proverbs 13:20", "Proverbs 14:12",
    "Proverbs 17:22", "Proverbs 20:24", "Proverbs 21:21", "Proverbs 24:16",
    "Proverbs 25:28", "Proverbs 28:13", "Proverbs 29:18", "Proverbs 30:5",
    "Proverbs 31:25",

    # Prophets
    "Isaiah 1:18", "Isaiah 6:8", "Isaiah 9:6", "Isaiah 12:2",
    "Isaiah 43:18-19", "Isaiah 46:4", "Isaiah 54:17", "Isaiah 58:11",
    "Isaiah 60:1", "Isaiah 64:8", "Jeremiah 1:5", "Jeremiah 29:13",
    "Jeremiah 31:3", "Jeremiah 32:17", "Lamentations 3:25-26",
    "Ezekiel 34:26", "Ezekiel 36:26", "Daniel 3:17-18", "Hosea 6:3",
    "Joel 2:25", "Amos 5:24", "Micah 6:8", "Micah 7:8",
    "Zephaniah 3:17", "Haggai 2:9", "Zechariah 4:6", "Malachi 3:10",

    # Gospels
    "Matthew 5:4", "Matthew 5:9", "Matthew 6:34", "Matthew 7:7",
    "Matthew 9:37-38", "Matthew 10:29-31", "Matthew 16:26", "Matthew 17:20",
    "Matthew 19:26", "Matthew 22:37-39", "Matthew 25:21", "Matthew 25:40",
    "Matthew 28:19-20", "Mark 10:27", "Mark 12:30-31", "Mark 16:15",
    "Luke 6:31", "Luke 6:38", "Luke 11:9", "Luke 15:7",
    "Luke 18:27", "Luke 19:10", "John 1:1", "John 4:24",
    "John 6:35", "John 8:12", "John 8:32", "John 10:10",
    "John 10:27-28", "John 11:25-26", "John 14:6", "John 15:5",
    "John 20:29",

    # Acts & Epistles
    "Acts 1:8", "Acts 2:38", "Acts 20:35", "Romans 1:16",
    "Romans 8:18", "Romans 8:31", "Romans 12:1", "Romans 12:12",
    "1 Corinthians 1:18", "1 Corinthians 6:19-20", "1 Corinthians 10:13",
    "1 Corinthians 15:57", "1 Corinthians 16:14", "2 Corinthians 4:16-18",
    "2 Corinthians 9:7", "Galatians 3:28", "Ephesians 1:7", "Ephesians 3:20",
    "Ephesians 4:32", "Philippians 1:6", "Philippians 2:3-4", "Philippians 4:8",
    "Colossians 1:17", "Colossians 2:6-7", "Colossians 3:2",
    "1 Thessalonians 5:11", "2 Thessalonians 3:3", "1 Timothy 4:12",
    "2 Timothy 2:15", "2 Timothy 4:7", "Hebrews 4:16", "Hebrews 10:23-25",
    "Hebrews 13:5", "Hebrews 13:8", "James 1:12", "James 1:17",
    "James 1:19", "James 4:7", "James 4:8", "1 Peter 3:15",
    "2 Peter 1:3", "2 Peter 3:9", "1 John 3:18", "1 John 5:4",
    "Jude 1:24-25", "Revelation 3:20", "Revelation 21:4", "Revelation 21:5",
    "Revelation 22:13",
]

# Remove any accidental duplicates while preserving order
VERSES = list(dict.fromkeys(VERSES))

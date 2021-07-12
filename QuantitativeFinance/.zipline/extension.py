import pandas as pd

from zipline.data.bundles import register
from zipline.data.bundles.csvdir import csvdir_equities

start_session = pd.Timestamp('2017-01-03', tz='utc')
end_session = pd.Timestamp('2021-06-29', tz='utc')

# register the bundle 
register(
    'apple-prices-2017-2021', # name we select for the bundle
    csvdir_equities(
        ['daily'], # name of the directory as specified above (named after data frequency)
        '/projects', # path to directory containing the data
    ),
    calendar_name='NYSE',  # US equities
    start_session=start_session,
    end_session=end_session
)

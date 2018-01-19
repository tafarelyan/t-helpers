import os

from t_helpers import *

#  sptrans = SPTrans()
#  sptrans.bus_position('709A-10')
#  sptrans.bus_estimate_time('709A-10')

#  import pandas as pd #  df = pd.read_csv('sptrans/stops.txt')

#  lat, lon = -23.5963908, -46.6885377

#  df['distance'] = ((df.stop_lat - lat) ** 2 + (df.stop_lon - lon) ** 2) ** .5

#  print(df.sort_values('distance')
#        .drop(['stop_desc', 'stop_lat', 'stop_lon', 'distance'], axis=1)
#        .head(10))

with Decolar() as decolar:
    decolar.get_flights('sao paulo', 'toronto')
    decolar.send_push()

mailing = Mailing('arrowsXmailbot@gmail.com', 'h@ck1tPlz')
mailing.send('tafarel.yan@gmail.com', 'Test', '')

print(tomo_chan_tracker())
print(shokugeki_no_soma_tracker())

send_push_notification('Test', '')
send_push_notification('Test link', '', 'https://www.google.com')

create_chatbot()
os.remove('bot.py')

download_from_youtube('Zedd Find you teaser')

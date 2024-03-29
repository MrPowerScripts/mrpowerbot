import json
import random
from os.path import exists

# accounts
MRPOWERBOT=733402362852540516

# roles
MOD_ROLE=534511381341405184
STREAMER_ROLE=733468896828457001
ROUNDTABLE_ROLE=741356984531550311
MONSTERS_ROLE=747205194927833099
MRPOWER_ROLE=534137759980584980
REDDIT_NOTIFY_ROLE=794158498769272842

# channels
LOG_CHANNEL=733415315035390064
MRPS_GUILD=510821302773219331
TEST_CHANNEL=747059994071007302
MRPSTY_CHANNEL=714447464219934822
MED_CHANNEL=510821302773219337
MRPSBOT_CHANNEL=733415265894662205
REDDIT_BOT_CHANNEL=697805367782146198
ANNOUNCE_CHANNEL=533049764472815626

if exists("/etc/heroku/dyno"):
  dyno_data = open("/etc/heroku/dyno").read()
  print(dyno_data)
  dyno_data = json.loads(dyno_data)
  REVISION = dyno_data.get("release").get("commit")[0:7]
else:
  REVISION = "local"

def prob(probability):
  rando = random.random()
  #print("prob: " + str(probability) + " rolled: " + str(rando))
  return rando < probability



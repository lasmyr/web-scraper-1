import yaml
import time

ref=yaml.load(open('.\\scripts\\params.yaml', 'r'), Loader=yaml.SafeLoader)
# print(ref.get('urls').get('main'))
# print(ref.get('urls').get('main')+ref.get('urls').get('subdir').get('stocks'))

print(
    ref.get('outpaths').get('prepped').format(
    time.localtime().tm_year
    , time.localtime().tm_mon
    , time.localtime().tm_mday
    , time.localtime().tm_hour
    , time.localtime().tm_min
    )

)


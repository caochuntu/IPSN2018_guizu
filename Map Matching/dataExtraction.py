import csv

def _unmatched_extraction():
    observations_raw = 'directory:\\your\\data\\containing\\latitude\\and\\longitude.csv'
    observations_result = 'directory:\\your\\map\\matching\\results.csv'
    observations_unmatched = 'Directory:\\final\\file\\containing\\only\\unmatched\\data.csv'

    with open(observations_result) as f_o:
        ref = []
        for i, line in enumerate(f_o):
            if i == 0:
                ref.append(0)
                continue
            line_length = line.split(',')
            if len(line_length) < 2:
                ref.append(1)
            else:
                ref.append(0)

        with open(observations_unmatched, 'w') as f_u:
            with open(observations_raw) as f_r:
                for i, line in enumerate(f_r):
                    if ref[i] == 1:
                        f_u.write(line)
            print ('matched data removed')
            f_r.flush()
            f_r.close()
        f_u.flush()
        f_u.close()

    f_o.flush()
    f_o.close()
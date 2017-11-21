import sys
import os
import time

if __name__ == '__main__':
  days = 5
  base_dir = os.getcwd()

  # save results to a separate dir
  folder = "test_{}".format(int(round(time.time() * 1000)))
  print("\n\n=== saving test results to {} ===\n".format(folder))
  os.mkdir(folder)
  os.chdir(folder)
  
  while days > 0:
    day = 6 - days
    print("\n### starting sessions for day {} ###\n".format(day))  
    if (day == 1):
      input_ac = "day0_account.txt"
      input_ma = "day0_master.txt"
      # create empty master and account files on first day
      os.system("touch {} {}".format(input_ac, input_ma))
    else:
      # on other days, use the accounts file and master accounts file
      # from the previous day to run a the daily script
      input_ac = output_ac
      input_ma = output_ma
    output_ac = "day{}_account.txt".format(day)
    output_ma = "day{}_master.txt".format(day)

    # run the daily script with input accounts file, input master file and output accounts file, output master file
    os.system("python {} {} {} {} {}".format(os.path.join(base_dir, 'daily_script.py'), input_ac, input_ma, output_ac, output_ma))
    days = days - 1

  # just remember to chdir back to the original dir 
  # in case we want to do other work there later, we dont
  # have to...
  os.chdir(base_dir)

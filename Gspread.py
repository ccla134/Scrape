import gspread

gc = gspread.service_account(filename='Creds.json')
sh = gc.open('TestScrapeSheet1')
sh = sh.get_worksheet(2)

sh.update('C' + str(2) + ':F' + str(2), [[1,2,3,4]])




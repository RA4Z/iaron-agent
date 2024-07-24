import xlwings as xw

def automate(worksheet: str, script: str):
    wb = xw.Book(worksheet)
    macro = wb.macro(script)
    macro()
    wb.save()

    if len(wb.app.books) == 1:
        wb.app.quit()

    else:
        wb.close()

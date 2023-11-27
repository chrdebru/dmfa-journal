from datetime import datetime
import math

@udf(
    fun_id='http://kg.socialsecurity.be/fun#YesNoToBoolean',
    text='http://users.ugent.be/~bjdmeest/function/grel.ttl#valueParam')
def yesNoToBoolean(text):
    return "1" if text.upper().strip() == 'YES' else "0"

@udf(
    fun_id='http://kg.socialsecurity.be/fun#FormatDate',
    text='http://users.ugent.be/~bjdmeest/function/grel.ttl#valueParam')
def formatDate(text):
    d = datetime.strptime(text, '%d/%m/%Y')
    return d.strftime('%Y-%m-%d')

@udf(
    fun_id='http://kg.socialsecurity.be/fun#QuarterFromDate',
    text='http://users.ugent.be/~bjdmeest/function/grel.ttl#valueParam')
def quarterFromDate(text):
    d = datetime.strptime(text, '%d/%m/%Y')
    return f"{d.strftime('%Y')}{math.ceil(d.month / 3)}"
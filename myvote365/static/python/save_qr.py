
import segno

def save_qr(short_id_num, color='#000', background='#F00', url='media/qr-codes/'):
    path = url + short_id_num + '.svg'
    content = 'https://myVote365.com/' + short_id_num + '/'
    qr = segno.make(content=content, error='M')
    qr.save(path, border=0, color=color)
    print('qr saved at \'{}\''.format(path))

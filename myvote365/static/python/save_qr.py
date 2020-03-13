
import segno


def save_qr(short_id_num, color='#000', background='#FFF', url='media/qr-codes/'):
    path = url + short_id_num + '.svg'
    content = 'https://myVote365.com/' + short_id_num + '/'
    qr = segno.make(content=content, error='H')
    qr.save(path, border=4, color=color, background=background)
    print('qr saved at \'{}\''.format(path))

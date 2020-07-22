from qcloudsms_py import SmsSingleSender
from saas_platform import settings


def send_sms_single(phone_num, tpl, template_param_list):
    '''
    # summary: 发送短信
    :param phone_num:   手机号
    :param tpl: 腾讯云短信模板ID
    :param template_param_list: 短信模板参数
    :return:
    '''
    appid = settings.APP_ID
    appkey =settings.APP_KEY
    sms_sign = settings.SMS_SIGN
    template_id = settings.TEMLPATE_ID_DICT[tpl]

    sender = SmsSingleSender(appid, appkey)
    try:
        response = sender.send_with_param\
            (86, str(phone_num), template_id, template_param_list, sign=sms_sign)
    except:
        response = {'result': 1000, 'errmsg': "网络异常发送"}
    return response


if __name__ == '__main__':
    res = send_sms_single(15552217716, 'register', [666,])
    print(res)
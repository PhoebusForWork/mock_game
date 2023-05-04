from base64 import b64decode, b64encode
from Crypto.Cipher import AES


class AESCipher:
    def __init__(self, secret_key):
        self.key = secret_key.encode(encoding="utf-8")

    def encrypt(self, text):
        self.cipher = AES.new(self.key, AES.MODE_ECB)
        text_padding = self.pkcs7padding(text)
        encrypt_data = self.cipher.encrypt(text_padding.encode(encoding="utf-8"))
        result = str(b64encode(encrypt_data), encoding='utf-8')
        return result

    def decrypt(self, text):
        self.cipher = AES.new(self.key, AES.MODE_ECB)
        raw = b64decode(text)
        decrypt_data = self.cipher.decrypt(raw)
        result = self.pkcs7unpadding(str(decrypt_data, encoding='utf-8'))
        return result

    @staticmethod
    def pkcs7padding(text):
        """
        明文使用PKCS7填充
        最终调用AES加密方法时，传入的是一个byte数组，要求是16的整数倍，因此需要对明文进行处理
        :param text: 待加密内容(明文)
        :return:
        """
        bs = AES.block_size  # 16
        length = len(text)
        bytes_length = len(bytes(text, encoding='utf-8'))
        padding_size = length if (bytes_length == length) else bytes_length
        padding = bs - padding_size % bs
        padding_text = chr(padding) * padding
        return text + padding_text

    @staticmethod
    def pkcs7unpadding(text):
        """
        处理使用PKCS7填充过的数据
        :param text: 解密后的字符串
        :return:
        """
        length = len(text)
        unpadding = ord(text[length - 1])
        return text[0:length - unpadding]


if __name__ == '__main__':
    key = "L8IbnjHo8OTu+LBwjQA4dw=="
    content = {
                  "loginName": "daotest001",
                  "nickName": "daotest001",
                  "headImg": "",
                  "wid":"1",
                  "merchantPayNo": "dao0707test001",
                  "amountStr":"[{\"walletType\":\"1\",\"amount\":\"100\"},{\"walletType\":\"2\",\"amount\":\"100\"},{\"walletType\":\"3\",\"amount\":\"1000000\"}]"
                }
    c = AESCipher(secret_key=key)
    encrypted_content = (c.encrypt(text=str(content)))
    print(f"encrypted_content: {encrypted_content}")
    # encrypted_content = "7502A321F7202C33550EE242DFAC8A3279DD33DF2AC5059070CC69517D9D31DF"
    decrypted_content = eval(c.decrypt(text=encrypted_content))
    print(f"decrypted_content: {decrypted_content}")
    # print(f"login name: {decrypted_content['loginName']}")



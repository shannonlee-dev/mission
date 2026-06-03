CAESAR_PASSWORD_TEXT = 'b ehox Ftkl sdlkf alk sdklfn' 


def caesar_cipher_decode(text):
   result = []
  
   for i in range(0, 26):
       decoded_text = ''
       for char in text:


           if 'a' <= char <= 'z':


               num = (ord(char)) - i
               if num < 97:
                   num += 26
               decoded_text += chr(num)  


           else :                 
               decoded_text += char  
              


       result.append(decoded_text)


   return result


def main():
   try:
       decode_passwords = caesar_cipher_decode(CAESAR_PASSWORD_TEXT)
      
       for i, password in enumerate(decode_passwords):
           print(f"{i}: {password}")
      
       result = int(input())
     
       if not 0 <= result <= 25:
           raise ValueError


       print(f"Result: {decode_passwords[result]}")


   except ValueError:
       print(f'invalid input.')
       return
   except Exception:
       print(f'error')
       return


if __name__ == '__main__':
   main()

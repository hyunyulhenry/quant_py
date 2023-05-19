from slack_sdk import WebClient

slack_token  = 'xoxb-3201556049680-3232837627973-fvhWHIWoNkJMMdgcmNvtHaMi'
client = WebClient(token=slack_token)

client.chat_postMessage(channel='#api_test',
                        text='Test message from python slack api')

client.files_upload(channels='#api_test',
                    file='C:/Users/doomoolmori/Dropbox/My Book/quant_python/test.xlsx',
                    filename='excel.xlsx',
                    filetype='xlsx')
import creds
import gmail_reader as gr
import sheet_writer as sw

credentials = creds.create_creds()
#order = gr.main(credentials)
order = 'me'
sw.main(credentials, order)

print ('done')

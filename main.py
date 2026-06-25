import creds
import gmail_reader as gr
import sheet_writer as sw

credentials = creds.create_creds()
#output = gr.main(credentials)
sw.main(credentials)

print ('done')

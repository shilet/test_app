import flet
import requests
import bs4
import os
import pdfkit

def main(page: flet.Page):
    # Your Flet application code here
    page.add(flet.Text("Hello, world!"))


flet.app(target=main, view=None)


def make_html(url, name):

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Save the content of the response as an HTML file
        soup = bs4.BeautifulSoup(response.content, 'html.parser')

        # Find the div with id "hormenu" and remove it
        hormenu_span = soup.find('span', id='hormenu_ver')
        if hormenu_span:
            hormenu_span.decompose()

        hormenu_span = soup.find('span', id='hormenu_hor')
        if hormenu_span:
            hormenu_span.decompose()

        rm_div = soup.find('div', id='headernieuw')
        if rm_div:
            rm_div.decompose()

        # Find the div with id "hormenu" and remove it
        #inhoud = soup.find('div', id='inhoudje')
        #if inhoud:
        #    inhoud.decompose()

        # Find and remove the <head> section
        #head = soup.find('head')
        #if head:
        #    head.decompose()

        htmlname = name + '.html'
        with open(htmlname, 'w', encoding='utf-8') as file:
            file.write(str(soup))
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")


def process_files(dirname):
    base_url = "https://www.stecr.nl/default.asp?"

    for file in os.listdir(dirname):
        if "@" in file:
            # Split the filename on "@" and extract the relevant parts
            _, params = file.split("@", 1)
            urlname = base_url + params

            # Find the 'name=' part and replace spaces with underscores for the filename
            name_index = params.find("name=")
            if name_index != -1:
                # Extract everything after 'name='
                name_part = params[name_index + 5:]
                # Replace spaces with underscores and remove illegal characters for filenames
                filename = name_part.replace(" ", "_").replace("(", "").replace(")", "").replace("&", "_and_")
                # Call your function with the constructed urlname and filename
                make_html(urlname, filename)



dirname = 'D:/Dropbox/sheila/bedrijfsgeneeskunde/nvab/stecr/stecr.nl'
process_files(dirname)
htmldir = 'D:/Dropbox/sheila/bedrijfsgeneeskunde/nvab/stecr/html'
full_file_paths = [os.path.join(htmldir, filename) for filename in os.listdir(htmldir)]
pdf_output = 'D:/Dropbox/sheila/bedrijfsgeneeskunde/nvab/stecr/output.pdf'  # The name of the combined PDF file

# Convert each HTML file to PDF and combine them
pdf_options = {
    'toc': '',  # This enables the TOC
    'toc-header-text': 'Table of Contents',  # Custom header for TOC
    'toc-level-indentation': '4em',  # Indentation for TOC levels
    'toc-text-size-shrink': 0.8,  # Shrink the TOC text size
}

full_file_paths = ['D:/Dropbox/sheila/bedrijfsgeneeskunde/nvab/stecr/html\\Artrose.html', 'D:/Dropbox/sheila/bedrijfsgeneeskunde/nvab/stecr/html\\Buikhernia.html']
#url = 'https://www.stecr.nl/default.asp?page_id=232&name=Hiv/aids'
### combine html files
#filelist = os.listdir(htmldir)
combined_soup = bs4.BeautifulSoup('<html><head><title>Combined Document</title></head><body></body></html>', 'html.parser')
body = combined_soup.body
output_html = htmldir + '/' + 'combined_document.html'
for file in full_file_paths:
    #    filename = htmldir + '/' + file
    with open(file, 'r', encoding='utf-8') as f:
        chapter_soup = bs4.BeautifulSoup(f, 'html.parser')
        # Find the specific content element
        chapter_title_text = os.path.splitext(os.path.basename(file))[0]
        # Create an anchor for the chapter title
        chapter_anchor = combined_soup.new_tag('a', id=chapter_title_text)
        body.append(chapter_anchor)
        chapter_title = combined_soup.new_tag('h1')
        chapter_title.string = chapter_title_text
        body.append(chapter_title)

        content_div = chapter_soup.find('div', {'id': 'inhoudje'})  # Target the specific div
        if content_div:
            # Find the h3 tag inside the content div to use as the chapter title
            for element in content_div.contents:
                print(element)
                body.append(element)

# Save the combined document to an HTML file
with open(output_html, 'w', encoding='utf-8') as f:
    f.write(str(combined_soup.prettify()))
pdfkit.from_file(output_html, pdf_output, toc='', verbose=True)


# Convert the combined HTML file to a PDF with TOC
toc = {
    "toc-header-text": "TOC title",
}
toc_options = {
    'toc-header-text': 'Table of Contents',
    'toc-level-indentation': '4em',

}
pdf_options = {
    'enable-internal-links': '',
    'outline-depth': '1',
#    'dump-default-toc-xsl':''
}
# Convert the combined HTML file to a PDF with TOC
pdfkit.from_file(output_html, pdf_output, options=pdf_options, toc=toc_options)

pdfkit.from_file(full_file_paths, pdf_output, options=pdf_options, toc=toc_options)



pdfkit.from_file(output_html, pdf_output, options={'enable-internal-links': ''}, toc=toc_options)
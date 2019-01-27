MangaTown Download Script
========================

# About

Created with the code base of MangaFox Download Script, changed so it can download from MangaTown

The Advantage of MangaTown is that the pages are not watermarked.

* Original MangaFox

 https://github.com/techwizrd/MangaFox-Download-Script

* My fork of MangaFox

 https://github.com/odrevet/MangaFox-Download-Script

# Dependencies

  * Python 3.3 or better
  * BeautifulSoup (``pip install beautifulsoup4``)

Tested on Arch Linux. It should work on any Linux, OS X, or Windows machine as long as the dependencies are installed.

# Usage

<pre>
Mandatory argument:
  -m --manga <Manga Name>

 Optional Arguments:
   -s Start At Chapter
   -e End At Chapter
   -c Create cbz Archive
   -r Remove image files after the creation of cbz archive
   -l List Chapters
</pre>

the MANGA_NAME parameter is located in the browser URL e.g www.mangatown.com/manga/xxxx/

To download an entire series:

    ~ $ python mtdl.py -m MANGA_NAME

To download a specific chapter:

    ~ $ python mtdl.py -m MANGA_NAME -s CHAPTER -e CHAPTER

To download a range of manga chapter:

    ~ $ python mtdl.py python mfdl.py -m MANGA_NAME -s CHAPTER_START -e CHAPTER_END

# Examples

* List chapters

    ~ $ python mtdl.py -m "xxxx" -l

* Download all of XXXX:

    ~ $ python mtdl.py -m "xxxx"

* Download chapter 222.5:

    ~ $ python mtdl.py -m "xxxx" -s 222.5 -e 222.5

* Download from chapter:

    ~ $ python mtdl.py -m "xxxx" -s 222.5

* Download chapters 190-205:

    ~ $ python mtdl.py -m "xxxx" -s 190 -e 205

# Notes

Please do not overuse and abuse this and destroy MangaTown. If you've got some cash, why not donate some to them and help them keep alive and combat server costs? I really would not like people to destroy MangaTown because of greedy downloading. Use this wisely and don't be evil.

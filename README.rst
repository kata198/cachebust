cachebust
=========


Cachebust provides a server-side means to ensure that clients always fetch assets when they are updated on the server.


Many browsers have different means of caching, some will overcache, and using the HTTP cache headers, there's always a chance you may need to update within the lifetime of the previous scripts.


cachebust provides a means to ensure that all assets are fetched by browsers when they are updated. The way it works, is that it takes HTML (via a library or commandline tool) and modifies the asset hrefs, adding a parameter "cachebust" equal to the md5sum of the file.

When the file changes, the md5sum will change, and the browser sees this as a distinct document, and will fetch the update no matter what its caching policy.


**Usage**


	Usage: cacheBust (options) [input]


	  Options:



		 \-r or \-\-asset-root       Specify the filesystem root which should be treated as "/" for links. Default is cwd

		 \-e or \-\-encoding         Specify the encoding to use (default, utf-8)

		 \-q or \-\-quiet            Do not print errors to stderr when cannot cachebust an element


		 \-\-help                   Show this message



**Library Documentation**


Can be found at: http://htmlpreview.github.io/?https://github.com/kata198/cachebust/blob/master/doc/cachebust.html

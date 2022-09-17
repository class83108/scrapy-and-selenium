#scrapy
#selenium

scrapy爬取的網站是https://m.coa.gov.tw/Transaction/FeedRawMaterialPrice/Index

透過控制台觀察到數據是透過post請求響應，因此對其進行抓包，再用xpath抓下來

selenium爬取的網站是https://ndltd.ncl.edu.tw/cgi-bin/gs32/gsweb.cgi/ccd=LZYthM/login?jstimes=1&loadingjs=1&o=dwebmge&allowkey=/tmp/%5Enclcdr__doschk/b_9uhM_1663431156__NDIwMDky&ssoauth=1&cache=1663431161741

因為規則可能寫在js中，我觀察不出規律，所以乾脆用selenium來爬取。比較要注意的是這個網站跑很慢，所以我用sleep來讓它跑，如果不sleep就會變成網站還沒跑出來所以xpath抓不到東西

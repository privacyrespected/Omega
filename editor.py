insertion= '\n <script type="text/javascript" src="main.js"></script>' + '\n'+ '<script type="text/javascript" src="/eel.js"></script>' +'\n' +'<link rel="stylesheet" href="plot.css">'+'<button type="button" class="menuitem" id="back" onclick="backhome()"><p class="caption">>Exit</p></button>'
with open('stock_sentiment.html','r',errors='ignore') as f:
    lines = f.readlines()
lines.insert(-2,insertion +'\n')
with open('stock_sentiment.html','w') as f:
    f.writelines(lines)
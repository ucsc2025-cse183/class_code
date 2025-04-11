# HTML

required: html, head, body
in body: h1, h2, h3, h4, p, div, span, b, i, table, tbody, thead, tr, td, img, a, form, input, select, option, nav

<a href="http://...">click me</a>
<img src="http://..."/>
<div style="....">

# styles

border: 20px 15ps  10px   5px  solid red;
        top  right bottom left color
margin: 20px;
padding: 10px;
color: black;
background: white;        
background-image: url("http://....")
display: block, inline, inline-block, none
opacity: 0.5;

# Location of CSS
- in <div style="...">
- in <head><style>....</style</head>
- in files/mystyle.css and include them
  <link rel="stylesheet" href="css/bulma.css">


# Location of JS
- in <div onclick="alert('here I am')">
- in <script>alert('here I am')</script>
- in <script src="http://....js"></script>
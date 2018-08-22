#
reCOMM = r'<!--.*?-->'
reTRIM_closing = r'<{0}.*?>[\s\S]*?<\/{0}>'
reTRIM = r'<\/*{0}>'
reTRIM_class = r'<\/*{0}.*?>'

closing_tag_name = ["a", "select", "footer"]
class_tag_name = [
    "span", "i", "em", "del", "strong", "img",
    "sup", "sub", "input", "textarea", "a",
    "html", "select", "font"
]
# 内联标签和html格式字符串，替换为 ""
inline_tags = [
    "<!DOCTYPE html.*?>", "<!DOCTYPE HTML.*?>",
    '&#161;', '&#193;', '&#225;', '&#162;', '&#194;', '&#163;', '&#195;', '&#227;', "&#160;",
    '&#164;', '&#196;', '&#228;', '&#165;', '&#197;', '&#229;', '&#166;', '&#198;', '&#230;',
    '&#167;', '&#199;', '&#231;', '&#168;', '&#200;', '&#232;', '&#169;', '&#201;', '&#233;',
    '&#170;', '&#202;', '&#234;', '&#171;', '&#203;', '&#235;', '&#172;', '&#204;', '&#236;',
    '&#173;', '&#205;', '&#237;', '&#174;', '&#206;', '&#238;', '&#175;', '&#207;', '&#239;',
    '&#176;', '&#208;', '&#240;', '&#177;', '&#209;', '&#241;', '&#178;', '&#210;', '&#242;',
    '&#179;', '&#211;', '&#243;', '&#180;', '&#212;', '&#244;', '&#181;', '&#213;', '&#245;',
    '&#182;', '&#214;', '&#246;', '&#183;', '&#215;', '&#247;', '&#184;', '&#216;', '&#248;',
    '&#185;', '&#217;', '&#249;', '&#186;', '&#218;', '&#250;', '&#187;', '&#219;', '&#251;',
    '&#188;', '&#220;', '&#252;', '&#189;', '&#221;', '&#253;', '&#190;', '&#222;', '&#254;',
    '&#191;', '&#223;', '&#255;', '&#192;', '&#224;', '&#226;', "&#34;", "&#38;", "&#226;",
    "&#60;", "&#62;", "&THORN;", "&thorn;", "&iquest;", "&szlig;", "&yuml;", "&Agrave;",
    "&iexcl;", "&Aacute;", "&aacute;", "&cent;", "&circ;", "&acirc;", "&pound;", "&gt;", "&amp;",
    "&Atilde;", "&atilde;", "&curren;", "&Auml", "&auml;", "&yen;", "&ring;", "&nbsp;", "&quot;",
    "&aring;", "&brvbar;", "&AElig;", "&aelig;", "&sect;", "&Ccedil;", "&ccedil;", "&uml;",
    "&Egrave;", "&egrave;", "&copy;", "&Eacute;", "&eacute;", "&ordf;", "&Ecirc;", "&ecirc;",
    "&laquo;", "&Euml;", "&euml;", "&not;", "&Igrave;", "&igrave;", "&shy;", "&Iacute;", "&lt;",
    "&iacute;", "&reg;", "&Icirc;", "&icirc;", "&macr;", "&Iuml;", "&iuml;", "&deg;", "&ETH;",
    "&ieth;", "&plusmn;", "&Ntilde;", "&ntilde;", "&sup2;", "&Ograve;", "&ograve;", "&sup3;",
    "&Oacute;", "&oacute;", "&acute;", "&Ocirc;", "&ocirc;", "&micro;", "&Otilde;", "&otilde;",
    "&para;", "&Ouml;", "&ouml;", "&middot;", "&times;", "&times;", "&divide;", "&cedil;",
    "&Oslash;", "&oslash;", "&sup1;", "&Ugrave;", "&ugrave;", "&ordm;", "&Uacute;", "&uacute;",
    "&raquo;", "&Ucirc;", "&ucirc;", "&frac14;", "&Uuml;", "&uuml;", "&frac12;", "&Yacute;",
    "&yacute;", "&frac34;", "&agrave;",
]
inline_tags.extend([reTRIM_closing.format(i) for i in closing_tag_name])
inline_tags.extend([reTRIM_closing.format(i.upper()) for i in closing_tag_name])
inline_tags.extend([reTRIM_class.format(i) for i in class_tag_name])
inline_tags.extend([reTRIM_class.format(i.upper()) for i in class_tag_name])
inline_tags.extend([reTRIM.format(i) for i in ["b", "u", "B", "U"]])

block_tag_name = [
    "address", "center", "h1", "h2", "h3", "li", "tr", "td", "body",
    "h4", "h5", "h6", "p", "pre", "blockquote", "br", "dd", "dt", "th",
    "marquee", "ul", "ol", "dl", "table", "form", "div", "hr", "tbody"
]

block_tags = [reTRIM_class.format(i) for i in block_tag_name]
block_tags.extend([reTRIM_class.format(i.upper()) for i in block_tag_name])

# 换行标签
br_tag = r'<br.*?>'

// https://cdnjs.cloudflare.com/ajax/libs/tabletop.js/1.5.1/tabletop.min.js
!function(){"use strict";var e=!1;if("undefined"!=typeof process&&!process.browser){e=!0;var t=require("request".trim())}var s=!1,i=!1;try{var n=new XMLHttpRequest;"undefined"!=typeof n.withCredentials?s=!0:"XDomainRequest"in window&&(s=!0,i=!0)}catch(e){}var o=Array.prototype.indexOf,a=function(e,t){var s=0,i=e.length;if(o&&e.indexOf===o)return e.indexOf(t);for(;s<i;s++)if(e[s]===t)return s;return-1},h=function(t){return this&&this instanceof h?("string"==typeof t&&(t={key:t}),this.callback=t.callback,this.wanted=t.wanted||[],this.key=t.key,this.simpleSheet=!!t.simpleSheet,this.parseNumbers=!!t.parseNumbers,this.wait=!!t.wait,this.reverse=!!t.reverse,this.postProcess=t.postProcess,this.debug=!!t.debug,this.query=t.query||"",this.orderby=t.orderby,this.endpoint=t.endpoint||"https://spreadsheets.google.com",this.singleton=!!t.singleton,this.simpleUrl=!(!t.simpleUrl&&!t.simple_url),this.callbackContext=t.callbackContext,this.prettyColumnNames="undefined"==typeof t.prettyColumnNames?!t.proxy:t.prettyColumnNames,"undefined"!=typeof t.proxy&&(this.endpoint=t.proxy.replace(/\/$/,""),this.simpleUrl=!0,this.singleton=!0,s=!1),this.parameterize=t.parameterize||!1,this.singleton&&("undefined"!=typeof h.singleton&&this.log("WARNING! Tabletop singleton already defined"),h.singleton=this),/key=/.test(this.key)&&(this.log("You passed an old Google Docs url as the key! Attempting to parse."),this.key=this.key.match("key=(.*?)(&|#|$)")[1]),/pubhtml/.test(this.key)&&(this.log("You passed a new Google Spreadsheets url as the key! Attempting to parse."),this.key=this.key.match("d\\/(.*?)\\/pubhtml")[1]),/spreadsheets\/d/.test(this.key)&&(this.log("You passed the most recent version of Google Spreadsheets url as the key! Attempting to parse."),this.key=this.key.match("d\\/(.*?)/")[1]),this.key?(this.log("Initializing with key "+this.key),this.models={},this.modelNames=[],this.model_names=this.modelNames,this.baseJsonPath="/feeds/worksheets/"+this.key+"/public/basic?alt=",e||s?this.baseJsonPath+="json":this.baseJsonPath+="json-in-script",void(this.wait||this.fetch())):void this.log("You need to pass Tabletop a key!")):new h(t)};h.callbacks={},h.init=function(e){return new h(e)},h.sheets=function(){this.log("Times have changed! You'll want to use var tabletop = Tabletop.init(...); tabletop.sheets(...); instead of Tabletop.sheets(...)")},h.prototype={fetch:function(e){"undefined"!=typeof e&&(this.callback=e),this.requestData(this.baseJsonPath,this.loadSheets)},requestData:function(t,n){if(this.log("Requesting",t),e)this.serverSideFetch(t,n);else{var o=this.endpoint.split("//").shift()||"http";!s||i&&o!==location.protocol?this.injectScript(t,n):this.xhrFetch(t,n)}},xhrFetch:function(e,t){var s=i?new XDomainRequest:new XMLHttpRequest;s.open("GET",this.endpoint+e);var n=this;s.onload=function(){var e;try{e=JSON.parse(s.responseText)}catch(e){console.error(e)}t.call(n,e)},s.send()},injectScript:function(e,t){var s,i=document.createElement("script");if(this.singleton)t===this.loadSheets?s="Tabletop.singleton.loadSheets":t===this.loadSheet&&(s="Tabletop.singleton.loadSheet");else{var n=this;s="tt"+ +new Date+Math.floor(1e5*Math.random()),h.callbacks[s]=function(){var e=Array.prototype.slice.call(arguments,0);t.apply(n,e),i.parentNode.removeChild(i),delete h.callbacks[s]},s="Tabletop.callbacks."+s}var o=e+"&callback="+s;this.simpleUrl?e.indexOf("/list/")!==-1?i.src=this.endpoint+"/"+this.key+"-"+e.split("/")[4]:i.src=this.endpoint+"/"+this.key:i.src=this.endpoint+o,this.parameterize&&(i.src=this.parameterize+encodeURIComponent(i.src)),this.log("Injecting",i.src),document.getElementsByTagName("script")[0].parentNode.appendChild(i)},serverSideFetch:function(e,s){var i=this;this.log("Fetching",this.endpoint+e),t({url:this.endpoint+e,json:!0},function(e,t,n){return e?console.error(e):void s.call(i,n)})},isWanted:function(e){return 0===this.wanted.length||a(this.wanted,e)!==-1},data:function(){if(0!==this.modelNames.length)return this.simpleSheet?(this.modelNames.length>1&&this.debug&&this.log("WARNING You have more than one sheet but are using simple sheet mode! Don't blame me when something goes wrong."),this.models[this.modelNames[0]].all()):this.models},addWanted:function(e){a(this.wanted,e)===-1&&this.wanted.push(e)},loadSheets:function(t){var i,n,o=[];for(this.googleSheetName=t.feed.title.$t,this.foundSheetNames=[],i=0,n=t.feed.entry.length;i<n;i++)if(this.foundSheetNames.push(t.feed.entry[i].title.$t),this.isWanted(t.feed.entry[i].content.$t)){var a=t.feed.entry[i].link.length-1,h=t.feed.entry[i].link[a].href.split("/").pop(),l="/feeds/list/"+this.key+"/"+h+"/public/values?alt=";l+=e||s?"json":"json-in-script",this.query&&(l+="&tq="+this.query),this.orderby&&(l+="&orderby=column:"+this.orderby.toLowerCase()),this.reverse&&(l+="&reverse=true"),o.push(l)}for(this.sheetsToLoad=o.length,i=0,n=o.length;i<n;i++)this.requestData(o[i],this.loadSheet)},sheets:function(e){return"undefined"==typeof e?this.models:"undefined"==typeof this.models[e]?void 0:this.models[e]},sheetReady:function(e){this.models[e.name]=e,a(this.modelNames,e.name)===-1&&this.modelNames.push(e.name),this.sheetsToLoad--,0===this.sheetsToLoad&&this.doCallback()},loadSheet:function(e){var t=this;new h.Model({data:e,parseNumbers:this.parseNumbers,postProcess:this.postProcess,tabletop:this,prettyColumnNames:this.prettyColumnNames,onReady:function(){t.sheetReady(this)}})},doCallback:function(){0===this.sheetsToLoad&&this.callback.apply(this.callbackContext||this,[this.data(),this])},log:function(){this.debug&&"undefined"!=typeof console&&"undefined"!=typeof console.log&&Function.prototype.apply.apply(console.log,[console,arguments])}},h.Model=function(e){var t,s,i,n;if(this.columnNames=[],this.column_names=this.columnNames,this.name=e.data.feed.title.$t,this.tabletop=e.tabletop,this.elements=[],this.onReady=e.onReady,this.raw=e.data,"undefined"==typeof e.data.feed.entry)return e.tabletop.log("Missing data for "+this.name+", make sure you didn't forget column headers"),this.originalColumns=[],this.elements=[],void this.onReady.call(this);for(var o in e.data.feed.entry[0])/^gsx/.test(o)&&this.columnNames.push(o.replace("gsx$",""));for(this.originalColumns=this.columnNames,this.original_columns=this.originalColumns,t=0,i=e.data.feed.entry.length;t<i;t++){var a=e.data.feed.entry[t],h={};for(s=0,n=this.columnNames.length;s<n;s++){var l=a["gsx$"+this.columnNames[s]];"undefined"!=typeof l?e.parseNumbers&&""!==l.$t&&!isNaN(l.$t)?h[this.columnNames[s]]=+l.$t:h[this.columnNames[s]]=l.$t:h[this.columnNames[s]]=""}void 0===h.rowNumber&&(h.rowNumber=t+1),e.postProcess&&e.postProcess(h),this.elements.push(h)}e.prettyColumnNames?this.fetchPrettyColumns():this.onReady.call(this)},h.Model.prototype={all:function(){return this.elements},fetchPrettyColumns:function(){if(!this.raw.feed.link[3])return this.ready();var e=this.raw.feed.link[3].href.replace("/feeds/list/","/feeds/cells/").replace("https://spreadsheets.google.com",""),t=this;this.tabletop.requestData(e,function(e){t.loadPrettyColumns(e)})},ready:function(){this.onReady.call(this)},loadPrettyColumns:function(e){for(var t={},s=this.columnNames,i=0,n=s.length;i<n;i++)"undefined"!=typeof e.feed.entry[i].content.$t?t[s[i]]=e.feed.entry[i].content.$t:t[s[i]]=s[i];this.prettyColumns=t,this.pretty_columns=this.prettyColumns,this.prettifyElements(),this.ready()},prettifyElements:function(){var e,t,s,i,n=[],o=[];for(t=0,i=this.columnNames.length;t<i;t++)o.push(this.prettyColumns[this.columnNames[t]]);for(e=0,s=this.elements.length;e<s;e++){var a={};for(t=0,i=this.columnNames.length;t<i;t++){var h=this.prettyColumns[this.columnNames[t]];a[h]=this.elements[e][this.columnNames[t]]}n.push(a)}this.elements=n,this.columnNames=o},toArray:function(){var e,t,s,i,n=[];for(e=0,s=this.elements.length;e<s;e++){var o=[];for(t=0,i=this.columnNames.length;t<i;t++)o.push(this.elements[e][this.columnNames[t]]);n.push(o)}return n}},"undefined"!=typeof module&&module.exports?module.exports=h:"function"==typeof define&&define.amd?define(function(){return h}):window.Tabletop=h}();

var TCH = TCH || {};
TCH.templateHtml = '<svg viewBox="0 0 100 55" width="100%">   <image height="30" width="30" x="35" y="-3" style="" xlink:href="data:image/png;base64,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" />   <ellipse cx="50" cy="25" rx="44" ry="23" style="fill:none;stroke:#fff;stroke-width:1" />   <text x="50" y="30" font-family="sans-serif" font-size="11px" fill="#fff" font-weight="bold" text-anchor="middle">%Players%</text>   <text x="50" y="38" font-family="sans-serif" font-size="5px" fill="#fff" text-anchor="middle">%Game%</text> </svg><br>';
TCH.renderActivity = function(publicSpreadsheetUrl, eleId)
{
    function _isOpenNow(hours) {
        return true;
        // function getMinuteValue(timeStr) {
        //  parts = timeStr.split(' ');
        //  parts[0] = parts[0].split(':');
        //  var mins = 60 * parts[0][0] + parts[0][1];
        //  if (parts[1]=='PM')
        //      mins += 12 * 60;
        //  return mins;
        //     }
        //     var now = new Date();
        //     var parts, mins;


        //     var offset = now.getTimezoneOffset();
        //     var offset = 0;

        //     var localOffset = 300;
        //     var bizHours = hours[now.getDay()];
        //     console.log(bizHours);
        //     var open = getMinuteValue(bizHours.Open);
        //     var close = getMinuteValue(bizHours.Close);
        //     if (close<open)

    }
    function _showInfo(wb, tabletop) {
        //isOpenNow(wb.Hours.elements);

        for(var i=0; i<wb.Activity.elements.length; i++){
            var row = wb.Activity.elements[i];
            var text = row.Players + ' Player' + (row.Players==1?'':'s');
            var html = TCH.templateHtml.replace('%Players%', text)
                .replace('%Game%', row.Game);
            document.getElementById(eleId).insertAdjacentHTML('beforeend', html);
        }
    }
    function _init() {
        Tabletop.init( { key: publicSpreadsheetUrl, callback: _showInfo, simpleSheet: false } );
    }
    window.addEventListener('DOMContentLoaded', _init);
}




// fix outside of biz hours
// 
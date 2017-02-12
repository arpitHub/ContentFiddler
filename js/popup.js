// Listen for messages
chrome.runtime.onMessage.addListener(function (msg, sender, sendResponse) {
    // If the received message has the expected format...
    if (msg.text === 'report_back') {
        // Call the specified callback, passing
        // the web-page's DOM content as argument
        var arr = [];
        for(var i = 0;i < document.getElementsByTagName('p').length;i++) {
          arr.push(document.getElementsByTagName('p')[i].textContent);
        }
        arr = arr.join(' ');
        arr = arr.replace(/(\r\n|\n|\r)/gm,".")
        $.ajax({
          type: "POST",
          cache: false,
          url: "http://localhost:8015/parsetext",
          // The key needs to match your method's input parameter (case-sensitive).
          data: {"paragraphs": arr},
          dataType: "json",
          success: function(data){
            obj = data;
            var sentences = [];
            for (var i = 0; i < obj.length; i++) {
              object = obj[i];
              var sentence = Object.keys(object)[0];
              if (undefined == sentence) {
                return
              }
              var sentObj = object[Object.keys(object)[0]];
              var newSent = sentence;
              for (var property in sentObj) {
                if (sentObj.hasOwnProperty(property)) {
                  var newpart = "<span title=\""+property+"\"><mark>"+sentObj[property]+"</mark></span>";
                  var tempSent = newSent;
            			newSent = newSent.split(property).join(newpart);
            			document.body.innerHTML = document.body.innerHTML.replace(tempSent.trim(), newSent.trim());
                }
              }
              sentences.push(newSent);
            }
          },
          failure: function(errMsg) {
              console.log(errMsg);
          }
        });
    }
});

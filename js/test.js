// A function to use as callback
function doStuffWithDom(document) {}

// When the browser-action button is clicked...
chrome.browserAction.onClicked.addListener(function (tab) {
    chrome.tabs.sendMessage(tab.id, {text: 'report_back'}, doStuffWithDom);
});

var divMap = new Object(); // holds PageReportEval objects indexed by divId
var hideControl;

function initDoc() {
  hideControl = new HideControl();

  for (var i = 0; i < idArray.length; i++) {
    divId = idArray[i];
    divMap[divId] = new PageReportEval(divId);
  }
}

function hideAll() {
  for (divId in divMap)
    divMap[divId].hide();
  hideControl.hide();
}

/*
 * HideControl constructor and methods
 */
function HideControl() {
  this.div = $('hideAll');
}

HideControl.prototype.hide = function() {
  for (divId in divMap)
    if (divMap[divId].isVisible) return;
  this.div.style.display = 'none';
}

HideControl.prototype.show = function() {
  this.div.style.display = 'block';
}

/*
 * PageReportEval constructor and methods
 */
function PageReportEval(divId) {
  if (!(this.div = $(divId)))
    throw Error('div with id: ' + divId + ' not found!');

  if (!(this.link = $(divId + 'a')))
    throw Error('link with id: ' + divId + 'a' + ' not found!');

  this.testId = divId + 'p';
  this.list = {};  // cache for retrieved responseText, indexed by evalResult
  this.index = {}; // last selected item for each list, indexed by evalResult

  // create references for use by event handlers
  var obj = this;
  var div = this.div;
  var link = this.link;

  // set tabindex dynamically
  this.div.setAttribute('tabindex', 0);

  if (document.addEventListener) {
    div.addEventListener('keydown', function(e) { divKeyDownHandler(e, obj) }, true);
    link.addEventListener('click', function(e) { linkClickHandler(e, obj) }, true);
  }
  else if (document.attachEvent) {
    var wrappedHandler1 = function(e) { if (!e) e = window.event; divKeyDownHandler.call(div, e, obj) }
    div.attachEvent('onkeydown', wrappedHandler1);
    var wrappedHandler2 = function(e) { if (!e) e = window.event; linkClickHandler.call(link, e, obj) }
    link.attachEvent('onclick', wrappedHandler2);
  }
}

PageReportEval.prototype.url = '/pgrpteval/';

PageReportEval.prototype.setContent = function(evalResult) {
  this.div.innerHTML = this.list[evalResult];
  hideControl.show();
}

PageReportEval.prototype.hide = function() {
  this.div.style.display = 'none';
  this.link.style.display = 'none';
  this.isVisible = false;
  if (this.hide.caller == null)
    hideControl.hide();
}

PageReportEval.prototype.show = function(evalResult) {
  this.div.innerHTML = 'Loading...';
  this.div.style.display = 'block';
  this.div.focus();

  this.link.style.display = 'inline';
  this.isVisible = true;

  if (!this.list[evalResult]) { // get content via Ajax request
    var params = '&testid=' + this.testId + '&eval=' + evalResult;
    var myAjax = new Ajax.Request (this.url, { method: 'get', parameters: params, onComplete: processResponse });
  }
  else { // list already fetched
    this.setContent(evalResult);
  }

  var thisObj = this; // needed for nested function
  function processResponse(originalRequest) {
    thisObj.list[evalResult] = originalRequest.responseText;
    thisObj.setContent(evalResult);
  }
}

/*
 * Top-level event handlers and helper functions
 */
function divKeyDownHandler(event, obj) {
  var KEY_UP = 38;
  var KEY_DOWN = 40;
  var code = event.keyCode;
  if (code != KEY_UP && code != KEY_DOWN) return true;

  var div = document.attachEvent ? this : event.currentTarget;
  var target = document.attachEvent ? event.srcElement : event.target;

  // if div has focus, simply allow default scrolling of list or page;
  // remove next line to allow KEY_DOWN to move to first item in list
  if (div == target) return true;

  var ul = div.getElementsByTagName('UL')[0];
  var items = ul.getElementsByTagName('LI');
  var count = items.length;
  var index = getTargetIndex(items, target);

  function preventDefault(e) {
    if (document.attachEvent)
      e.returnValue = false;
    else
      e.preventDefault();
  }

  switch(code) {
  case KEY_DOWN:
    if (index < count - 1) {
      setItemFocus(items, index + 1);
      preventDefault(event);
    }
    break;
  case KEY_UP:
    if (index > 0) {
      setItemFocus(items, index - 1);
      preventDefault(event);
    }
    break;
  }
  return false;
}

/*
 * @param items: list of li elements
 * @param index: offset in list to receive focus
 */
function setItemFocus(items, index) {
  var anchor = items[index].firstChild;
  anchor.focus();
}

/*
 * @param items: list of li elements
 * @param target: element that fired event
 */
function getTargetIndex(items, target) {
  var length = items.length;
  for (var i = 0, idx = 0; i < length; i++) {
    var anchor = items[i].firstChild;
    if (anchor == target) return idx;
    idx++;
  }
  return -1;
}

function linkClickHandler(event, obj) {
  var link = document.attachEvent ? this : event.currentTarget;
  var listItem = link.parentNode;
  var parentList = listItem.parentNode;
  var childLinks = parentList.getElementsByTagName('A');
  var nextToLast = childLinks.length - 2;
  childLinks[nextToLast].focus();
}

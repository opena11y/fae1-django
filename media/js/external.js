/*
 * addHandlers:
 *   Gets all 'a' tags with class 'external' and sets onclick and
 *   onkeypress handlers on those elements. Requires prototype.js
 */
function addHandlers() {
  var myArray = $$('a.external');
  for (var i = 0; i < myArray.length; ++i) {
    var item = myArray[i];
    item.onclick = function(event) { return launchWindow(this, event); }
    // UAAG requires that user agents handle events in a device-independent manner
    // but only some browsers do this, so add keyboard event to be sure
    item.onkeypress = function(event) { return launchWindow(this, event); }
  }
}
/*
 * launchWindow:
 *   Handles only keypress events from carriage return or space.
 *   Sets focus to new window.
 */
function launchWindow(objAnchor, objEvent) {
  var iKeyCode, bSuccess=false;

  // If the event is from a keyboard, we only want to open the
  // new window if the user requested the link (return or space)
  if (objEvent && objEvent.type == 'keypress')
  {
    if (objEvent.keyCode)
      iKeyCode = objEvent.keyCode;
    else if (objEvent.which)
      iKeyCode = objEvent.which;

    // If not carriage return or space, return true so that the user agent
    // continues to process the action
    if (iKeyCode != 13 && iKeyCode != 32)
      return true;
  }

  bSuccess = window.open(objAnchor.href);

  // If the window did not open, allow the browser to continue the default
  // action of opening in the same window
  if (!bSuccess)
    return true;

  // The window was opened, so stop the browser processing further
  bSuccess.focus()
  return false;
}

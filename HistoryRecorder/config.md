## Configuration

**`display-status`**

Display/hide status bar at the bottom of the window. Possible values: `true`, `false`.

---

**`enabled-by-default`** 

Recorder is enabled on startup - it means that whenever you open Anki, recorder will be enabled. If you prefer 
to have it disabled by default, set this option to `false`. 

Possible values: `true`, `false`. 
You can also enable/disable the recorder anytime using *"Tools -> History Recorder"* menu.

---

**`live-sync`**

Automatically send each answer to the cloud (in the background). Possible values: `true`, `false`.

---

**`region`**

Which server to use. Two possibilities are: `"us"` and `"eu"` for US and Europe respectively. Any other values will fallback to the `"eu"` by default.
Choosing a region closer to you means slightly faster communication with the cloud.

---

**`hide-stopwords`**

Do not display stopwords ("and", "the", "of", etc) in a word cloud in summary window.
This value can be `true`, `false`, or a `list` of string.

* If it's `false`, then stopwords are not skipped.
* If it's `true`, then stopwords from all supported languages are skipped.
* If it's a `list`, then each element should be a name of the language. Stopwords only from given languages will be skipped.

Following languages are supported (the list comes from NLTK project.):

* `arabic` 
* `azerbaijani` 
* `danish` 
* `dutch` 
* `english` 
* `finnish` 
* `german` 
* `greek` 
* `hungarian` 
* `nepali` 
* `french` 
* `italian` 
* `italian`
* `romanian`
* `indonesian`
* `portuguese`
* `swedish`
* `norwegian`
* `norwegian`
* `slovene`
* `russian`
* `tajik`
* `turkish`
* `spanish`

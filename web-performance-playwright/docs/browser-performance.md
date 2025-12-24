# Browser performance

## Browser rendering steps

### Navigation

- Latency is the biggest threat to our ability to ensure a fast-loading page.
- Browser performance is about minimizing main thread responsibilities and to ensure smooth rendering.
- Browser navigation consists of:
  1. DNS lookup
  2. TCP handshake
  3. TLS nagotiation

### Response

- This response for this initial request contains the first byte of data received - This is the Time to First Byte

### Parsing

- After navigating and receiving the first information browser begins the Parsing step - where he renders the DOM and CSSOM.
  - It is importnat that the browser has all the nescesary information it needs to render in the first 14kb information packet it gets from TTFB
- Rendering involves processign html and building the DOM. DOM rendering occupies the main thread.
- The preload parces goes through the html document and finds assets to download, these are the img and script tags in the document. We need to add async or defer attributes to script tags to free them form the main thread. Also the execution order here is important as well.
- After the dom CSSOM is parsed and processed. It builds up the parent child tree and adds styles based on its specifisity, in essence it _cascades_ the property values. CSSOM is generaly faster than the DNS lookup.
- Browser then does javascript compilation in the main thread, unless they are done in web workers.
- Accessibility tree is also built by creating the AOM - a semantic version of the DOM.

### Rendering

Rendering step involves rendering:

1. Style
2. Layout
3. Paint
4. Compositing

The DOM and CSSOM are combined into the rendering tree that is then computed into the layout and painted on the screen.

- At the paint step the _First Meaningful paint_ occurs.

### Interactivity

Since we add interactivity with javascript, the ability for the user to manipulate browser nodes comes in only after **onload** event is triggered. This can take some time if the main thread is busy, thus we might be unable to scroll, touch or interact with the site.

This is the _Time To Interactive_ (TTI) metric. It is the time from DNS lookup to when the page is interactive.

- it needs to be interactable in **50ms** adter first contentful paint.
- First Contentful Paint is deprecated and now Largest cContentful Paint is used.

## References

- [Populating the page: how browsers work - Performance | MDN](https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/How_browsers_work)

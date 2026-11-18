"""Pixel couch potato: writes website/favicon.svg, favicon-64.png, apple-touch-icon.png.
Edit ROWS (16x16) to redraw. # outline · o potato · h highlight · s eye/spot · n couch · l cushion"""
import os, subprocess, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROWS = [
  "................",
  "................",
  "....########....",
  "..##hhhoooooo##.",
  ".#hhooooooosoo#.",
  ".#hoosooooooooo#",
  "#oooooooooooooo#",
  "#ooooooooosoooo#",
  "n#ooosoooooooo#n",
  "nn############nn",
  "nnllllllllllllnn",
  "nnllllllllllllnn",
  "nnnnnnnnnnnnnnnn",
  ".n............n.",
  "................",
  "................",
]
PAL = {"#": "#2a1a0e", "o": "#c8894a", "h": "#e9bd84", "s": "#6b3e1c", "n": "#000080", "l": "#3a4bd8"}
assert all(len(r) == 16 for r in ROWS)
px = [(x, y, PAL[c]) for y, r in enumerate(ROWS) for x, c in enumerate(r) if c in PAL]
svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" shape-rendering="crispEdges">'
       + "".join(f'<rect x="{x}" y="{y}" width="1" height="1" fill="{c}"/>' for x, y, c in px) + "</svg>\n")
open(os.path.join(ROOT, "website", "favicon.svg"), "w").write(svg)
# PNGs via AppKit (no extra tools needed)
jxa = """ObjC.import('AppKit');
function run(a){ var px=JSON.parse(a[0]);
 [[a[1],64,0,'transparent'],[a[2],180,18,'#14110e']].forEach(function(spec){ var out=spec[0], S=spec[1], pad=spec[2], k=(S-2*pad)/16;
  var rep=$.NSBitmapImageRep.alloc.initWithBitmapDataPlanesPixelsWidePixelsHighBitsPerSampleSamplesPerPixelHasAlphaIsPlanarColorSpaceNameBytesPerRowBitsPerPixel(null,S,S,8,4,true,false,$.NSDeviceRGBColorSpace,0,0);
  $.NSGraphicsContext.saveGraphicsState; $.NSGraphicsContext.setCurrentContext($.NSGraphicsContext.graphicsContextWithBitmapImageRep(rep));
  function col(h){ return $.NSColor.colorWithSRGBRedGreenBlueAlpha(parseInt(h.substr(1,2),16)/255,parseInt(h.substr(3,2),16)/255,parseInt(h.substr(5,2),16)/255,1); }
  if(spec[3]!=='transparent'){ col(spec[3]).set; $.NSBezierPath.fillRect($.NSMakeRect(0,0,S,S)); }
  px.forEach(function(p){ col(p[2]).set; $.NSBezierPath.fillRect($.NSMakeRect(pad+p[0]*k, S-pad-(p[1]+1)*k, k, k)); });
  $.NSGraphicsContext.restoreGraphicsState;
  rep.representationUsingTypeProperties($.NSBitmapImageFileTypePNG,$({})).writeToFileAtomically(out,true); });
 return 'ok'; }"""
w = os.path.join(ROOT, "website")
print(subprocess.run(["osascript", "-l", "JavaScript", "-e", jxa, json.dumps(px),
                      os.path.join(w, "favicon-64.png"), os.path.join(w, "apple-touch-icon.png")],
                     capture_output=True, text=True).stdout.strip())

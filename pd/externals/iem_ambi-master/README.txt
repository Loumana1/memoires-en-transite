This library extends the performance of Miller S. Puckette's
realtime-computermusic-environment puredata (pd).

iem_ambi contains 1 external library "iem_ambi.dll" with 12 objects and their
help files (see CONTENT.txt). The main topics are ambisonics encoding/decoding/rotating and signal matrix multiplication.
Ambisonics is a 3D sound spatialisation system with separated encode and decode rendering, calculations are based on spherical harmonics.

iem_ambi is published under the Gnu Lesser General Public License
  (see LICENSE.txt and GnuLGPL.txt).

iem_ambi (Release 1.21) is written by Thomas Musil from IEM KUG Graz Austria
 and it is compiled against pd-0.48-1.

You have to add the library -lib iem_ambi (Menue: File: Preferences: Startup...: New...).

  For Windows "install_path" could be:
"C:/Users/xx_ME_xx/AppData/Roaming/Pd" or
"C:/Program Files (x86)/Common Files/Pd" or
"C:/Users/xx_ME_xx/Documents/Pd/externals" or
"C:/Program Files (x86)/pd/extra".

  For Apple OSX: "install_path" could be:
"~/Library/Pd" or
"/Library/Pd" or
"/Applications/Pd.app/Contents/Resources/extra".

  For Linux: "install_path" could be:
"~/.local/lib/pd/extra" or
"~/pd-externals" or
"/usr/local/lib/pd-externals" or
"/usr/local/lib/pd/extra" or
"/usr/lib/pd/extra".

Make sure that you get the desired version of iem_ambi if there are multiple installations on your computer (-verbose).



Copyright (C) 2000-2018 Thomas MUSIL [musil_at_iem.at]


THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY
EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE AUTHOR
BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
THE POSSIBILITY OF SUCH DAMAGE.



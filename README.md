# Numerical_Solver_in_Python_for_Soil_Infiltration_Tests

![Preview](https://numericalenvironmental.files.wordpress.com/2018/03/gui.png)

This is a short Python 3 script that uses the SciPy package’s integrate.odeint method to solve a set of coupled ordinary differential equations approximating the infiltration of a wetting front into unsaturated soil. It is intended to serve as a means for interpreting more complex infiltration tests than are commonly provided by analytical solution models employing idealized assumptions such as a steady-state ponding depth. A more complete discussion of the methodology and an example application are provided in my blog, https://numericalenvironmental.wordpress.com/2018/03/05/interpreting-a-non-steady-soil-infiltration-test-using-a-numerical-ode-solver/. The script requires the following Python libraries:
* SciPy
* Matplotlib (for comparing model results with a user-provided observation set)
* PyQt5 (to enable a simple GUI, provided as a side-project accompanying the numerical model)

In addition to the script itself (percolation.py), the following files are also required:
* params.txt – model parameter file (e.g., hydraulic conductivity, porosity, saturation, evaporation rate, initial water influx and cessation time, initial pond depth and wetting front extent, name of observation data set) that is used to run the model and is also read from, and written to, by the script’s GUI
* dataset.txt – transducer data file for the infiltration test, with time as the left column and pond depth the right column; “dataset” is the root name (user-defined) for the observation set, also listed under the params.txt file
* userInterface.ui – an XML file that defines the script’s GUI (editable by Qt-designer)

I'd appreciate hearing back from you if you find the code useful. Questions or comments are welcome at walt.mcnab@gmail.com.

THIS CODE/SOFTWARE IS PROVIDED IN SOURCE OR BINARY FORM "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.



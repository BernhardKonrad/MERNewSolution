from flask import Flask, request, render_template
import redis

redis = redis.StrictRedis(host = 'pub-redis-10073.us-east-1-3.3.ec2.garantiadata.com' , port = '10073' , db = 0)
app = Flask(__name__)

def tags():
    return ["Alternating series",\
"Alternating series estimation theorem",\
"Antiderivative sketching",\
"Arc length",\
"Area between two curves",\
"Asymptote",\
"Average value",\
"Binomial distribution",\
"Center of mass",\
"Centroid",\
"Cobwebbing",\
"Complex numbers",\
"Concavity",\
"Consumer surplus",\
"Continuity",\
"Cumulative distribution function",\
"Curve sketching",\
"Determinants",\
"Differential equation",\
"Differential equation (higher order)",\
"Differentiate",\
"Discrete probability",\
"Eigenvalues and eigenvectors",\
"Equation of a plane",\
"Equilibrium",\
"Euler's method",\
"Exact differential equation",\
"Expected value",\
"Exponential growth and decay",\
"Fundamental theorem of calculus",\
"Fundamental theorem of calculus (multivariable)",\
"Gaussian elimination",\
"Geometric linear algebra",\
"Geometric series",\
"Gradients",\
"Hooke's law",\
"Hydrostatic force",\
"Implicit differentiation",\
"Improper integral",\
"Initial value problem",\
"Integral comparison test",\
"Integral properties",\
"Integrals that cycle",\
"Integrating factor",\
"Integration by parts",\
"Integration using symmetry",\
"Intermediate value theorem",\
"Invertibility",\
"L'Hopital's rule",\
"Lagrange multipliers",\
"Laplace transforms",\
"Least squares",\
"Level curves",\
"Limit",\
"Limit of a function",\
"Linear approximation",\
"Linear independence (linear algebra)",\
"Linear ordinary differential equation",\
"Linear transformation",\
"MATLAB",\
"Marginal productivity",\
"Market equilibrium",\
"Mass",\
"Mathematical induction",\
"Matrix diagonalization",\
"Matrix operations",\
"Mean (continuous)",\
"Mean value theorem",\
"Median (continuous)",\
"Multivariable calculus",\
"Net change theorem",\
"Newton's law of cooling",\
"Newton's method",\
"Nullspace",\
"Optimization",\
"Orthogonal complement",\
"Orthogonal projection",\
"Partial derivative",\
"Partial fractions",\
"Polar coordinates",\
"Power series",\
"Probability density function",\
"Projections",\
"Random walks",\
"Rank and nullity",\
"Reflection",\
"Related rates",\
"Riemann sum",\
"Separation of variables",\
"Sequences",\
"Series",\
"Set theory",\
"Simpson's rule",\
"Solid of revolution",\
"Standard deviation (continuous)",\
"Steady states",\
"Steady states (sequences)",\
"Substitution",\
"Summations",\
"System of linear equations",\
"Tangent line",\
"Tangent plane",\
"Taylor's remainder theorem",\
"Taylor series",\
"Toricelli's law",\
"Trapezoidal rule",\
"Trigonometric integral",\
"Trigonometric substitution",\
"Variance",\
"Volume (cross section)",\
"Work"]

@app.route('/')
def hello():
#    name = redis.get('name').decode('utf-8')
    hint = redis.get('hint').decode('utf-8')
    sol = redis.get('sol').decode('utf-8')
    both = hint + sol
    my_tags = tags()
    return render_template("communicate.html", myhint='', mysol='', both=both, tags=my_tags)


@app.route('/', methods=['POST'])
def communicate_post():
    if request.form['submit'] == 'preview':
        hint = request.form['inputHint']
        sol = request.form['inputSol']
        redis.set('hint', hint)
        redis.set('sol', sol)
        both = hint + sol
        return render_template("communicate.html", myhint=hint, mysol=sol, both = both)
    else:
        return "Something went wrong"

if __name__ == "__main__":
	app.run(debug=True)

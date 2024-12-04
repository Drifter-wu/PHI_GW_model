$\Psi$ model is a non-general relativity full waveform for general parametrization of axisymmetric black holes. The model comprises two main components: an inspiral part obtained by using a phenomenological method in the frequency domain and a ringdown part derived from quasinormal modes associated with photon motion. The detailed information can be found in https://journals.aps.org/prd/abstract/10.1103/PhysRevD.108.083032

### Inspiral part

$\phi_{\mathrm{Ins}}=  \phi_{\mathrm{TF} 2}(M f ; \Xi)  +\frac{1}{\eta}\left(\sigma_{0}+\sigma_{1} f+\frac{3}{4} \sigma_{2} f^{4 / 3}+\frac{3}{5} \sigma_{3} f^{5 / 3}+\frac{1}{2} \sigma_{4} f^{2}\right)+\phi_{\mathrm{KRZ}}$


where $\eta=m_1 m_2/M^2$, $M = m_1+m_2$, the $\phi_{\mathrm{TF} 2}$ is the full TaylorF2 phase:

$\phi_{\mathrm{TF} 2}=  2 \pi f t_{c}-\varphi_{c}-\pi / 4  +\frac{3}{128 \eta}(\pi f M)^{-5 / 3} \sum_{i=0}^{7} \varphi_{i}(\Xi)(\pi f M)^{i / 3}$

The constants $\sigma_{i}$ (where $i = 0, 1, 2, 3, 4$) represent the correlation between the mass and spin of the system. Meanwhile, the phase deformation arising from the general parameterized black hole is denoted by $\phi_{\mathrm{KRZ}}$. Varying the values of $\delta_1$, $\delta_2$, $\delta_4$, and $\delta_6$ will result in different phases. $\varphi_{i}(\Xi)$ are the PN expansion coefficients that are related to the intrinsic binary parameters. 



### Intermediate part

The intermediate stage is after the inspiral stage, and its phase is given by

$\phi_{\mathrm{Int}}=\frac{1}{\eta}\left(\beta_0+\beta_1 f+\beta_2 \log (f)-\frac{\beta_3}{3} f^{-3}\right)$

$\beta_{i}(i=0, 1, 2, 3)$ is the constants related to the mass and spin of the system.



### Ringdown part
The real part of QNMs, $\omega_R$, can be decomposed into two directional components, namely, $\theta$ and $\phi$:

$\omega_R=L\Omega_{\theta}(m/L)+m\Omega_{\mathrm{prec}}(m/L)$
where $\Omega_{\theta}$ indicates the frequency of polar motion, which is the rate at which the photon oscillates above and below the equatorial plane. The oscillation period can be calculated using the formula, $T_{\theta}=2\pi/\Omega_{\theta}$.

In addition to polar motion, the particle also undergoes a periodic motion in the azimuthal ($\phi$) direction with respect to the oscillation period, $T_{\theta}$, and the magnitude, $\Delta \phi$. The deviation between $\Delta \phi$ and $\pm 2\pi$ is commonly known as the "precession angle":


$\Delta \phi_{\mathrm{prec} }=\Delta \phi +4\pi\quad(\mathrm{corotating \; orbit} )$ or $\Delta \phi_{\mathrm{prec} }=\Delta \phi -4\pi\quad(\mathrm{couterrotating \; orbit})$


$\Omega_{\mathrm{prec}}=\Delta\phi_{\mathrm{prec} }/T_{\theta}$

$L=l+1/2$.

The values of $l$ and $m$ could be determined through the conditions:
```math
V^{r}\left(r, \omega_{R}\right)=\left.\frac{\partial V^{r}}{\partial r}\right|_{\left(r, \omega_{R}\right)}=0,
```
and $V^r$ is the potential in the radial Teukolsky equation. The imaginary component of QNMs, $\omega_I$, is directly linked to the Lyapunov exponents, which determine the rate at which a circular null geodesic expands its cross-sectional area under infinitesimal radial perturbations. 

The amplitude of the gravitational wave can be expressed as follows
```math
{{\left| {{h}_{lm}} \right|}^{2}}\sim \frac{d}{dt}\left( {{\Omega }_{lm}}^{2} \right)\,,
```
where $\Omega_{lm}$ is the orbital frequency, through this equation, we can get the equation of the GW waveform:

```math
{h}_{22}=X \operatorname{sech}\left[\gamma\left(t-t_{p}\right)\right] e^{-i \tilde{\Phi}_{22}(t)}\,
```
The equation includes the following variables: $X$ is a constant related to the amplitude of the waveform, $\gamma$ is the Lyapunov exponent characterizing the rate of divergence of nearby null geodesics, $t_p$ is the time at maximum amplitude of the waveform and $\Phi_{22}(t)$ is the phase. 

We can also derive the phase equation:
```math
\tilde{\Phi}_{22}=& \int_{0}^{t} \Omega d t^{\prime}=\arctan _{+}+\operatorname{arctanh}_{+} \\
&-\arctan _{-}-\operatorname{arctanh}_{-}-\phi_0,
```

where
```math
\arctan _{\pm} \equiv \kappa_{\pm} \tau\left[\arctan \left(\frac{\Omega}{\kappa_{\pm}}\right)-\arctan \left(\frac{\Omega_{0}}{\kappa_{\pm}}\right)\right]\,, \\
\arctan \mathrm{h}_{\pm} \equiv \kappa_{\pm} \tau\left[\arctan h\left(\frac{\Omega}{\kappa_{\pm}}\right)-\arctan h\left(\frac{\Omega_{0}}{\kappa_{\pm}}\right)\right]
\end{array}\right.
```

\begin{equation}
\kappa_{\pm} \equiv\left\{\Omega_{0}^{4} \pm k\left[1 \mp \tanh \left(\frac{t_{0}-t_{p}}{\tau}\right)\right]\right\}^{1 / 4}\,,
\end{equation}


\begin{equation}\label{attention1}
\Omega=\left\{\Omega_{0}^{4}+k\left[\tanh \left(\frac{t-t_{p}}{\tau}\right)-\tanh \left(\frac{t_{0}-t_{p}}{\tau}\right)\right]\right\}^{1 / 4}\,,
\end{equation}

\begin{equation}\label{attention2}
k=\left(\frac{\Omega_{\mathrm{QNM}}^{4}-\Omega_{0}^{4}}{1-\tanh \left[\left(t_{0}-t_{p}\right) / \tau\right]}\right)\,,
\end{equation}\\
where $\tau=\gamma^{-1}$, ${{\Omega }_{\operatorname{QNM}}}$=$\omega_{\operatorname{QNM}}$/m($\Omega_{\operatorname{QNM}}$ is just $\omega_R$), and $\phi_0$, $\Omega_0$, $t_0$ are the constants that can be freely chosen.

We need to focus on Eqs.~(\ref{attention1}) and (\ref{attention2}) mentioned above. The inclusion of terms with an even power in these equations imposes an extra constraint on $\Omega_0$. Our objective is to determine the minimum value of $\Omega_0$, which can be achieved by equating the expression inside Eq.~(\ref{attention1}) to zero. This yields the following function:
\begin{equation}\label{attention3}
\Omega_{0}^{4}=k\left[-\tanh \left(\frac{t-t_{p}}{\tau}\right)+\tanh \left(\frac{t_{0}-t_{p}}{\tau}\right)\right]\,.
\end{equation}
Substituting Eq.~(\ref{attention2}) into Eq.~(\ref{attention3}), we can get the solution of Eq.~(\ref{attention3})(we only consider the positive solution):
\begin{equation}\label{Omega_min}
{{\Omega }_{0}}^{4}=\frac{{{\Omega }_{\text{QNM}}}^{4}(\tanh [\frac{t-{{t}_{p}}}{\tau }]-\tanh [\frac{{{t}_{0}}-{{t}_{p}}}{\tau }])}{(-1+\tanh [\frac{{{t}_{0}}-{{t}_{p}}}{\tau }])(1-\frac{\tanh [\frac{t-{{t}_{p}}}{\tau }]}{1-\tanh [\frac{{{t}_{0}}-{{t}_{p}}}{\tau }]}+\frac{\tanh [\frac{{{t}_{0}}-{{t}_{p}}}{\tau }]}{1-\tanh [\frac{{{t}_{0}}-{{t}_{p}}}{\tau }]})}\,.
\end{equation}\\

With Eq.~(\ref{Omega_min}), we get the minimum value of $\Omega_0$. For convenience, we choose $t$ equal to $t_p$, so Eq.~(\ref{Omega_min}) can be simplified to this form:
\begin{equation}\label{Omega_min_simplify}
{{\Omega }_{0}}^{4}={{\Omega }_{\text{QNM}}}^{4}(\tanh [\frac{{{t}_{0}}-{{t}_{p}}}{\tau }])\,.
\end{equation}\\
Thus, we obtain the minimum value of $\Omega_0$ is $\Omega_{\operatorname{QNM}}$(i.e. the region of $\Omega_0$ is $\Omega_0 \textgreater \Omega_{\operatorname{QNM}}$). 

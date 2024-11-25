#!/usr/bin/env python
"""
Tutorial to demonstrate running parameter estimation on GW150914

This example estimates all 15 parameters of the binary black hole system using
commonly used prior distributions. This will take several hours to run. The
data is obtained using gwpy, see [1] for information on how to access data on
the LIGO Data Grid instead.

[1] https://gwpy.github.io/docs/stable/timeseries/remote-access.html


edited by ysc

"""

###
import sys
sys.path.append("./lib")
from lib.source import lal_binary_black_hole_pv3, lal_binary_black_hole #自定义波形函数
##################################################################

import bilby
import numpy as np
from gwpy.timeseries import TimeSeries
from bilby.core.prior import Uniform, PowerLaw, LogUniform, Constraint
import datetime
from gwosc.datasets import event_gps, event_detectors

from multiprocessing import Pool
import random 
import time 

##需要修改的地方##############################################################################################################

def run(label, wave_function = lal_binary_black_hole):
    ###
    # merge时间
    trigger_time = event_gps(label)
    detectors = event_detectors(label)

    ## 改变prior 导入方式
    ##priors = bilby.gw.prior.BBHPriorDict(filename="GW150914.prior")
    time_of_event = trigger_time

    ### 15 + 1 对于不同事件需要调整！！！！！！
    prior = bilby.core.prior.PriorDict()
    prior['chirp_mass'] = Uniform(name='chirp_mass', minimum=30.0,maximum=32.5)#
    prior['mass_ratio'] = Uniform(name='mass_ratio', minimum=0.5, maximum=1)#
    prior['mass_1'] = Constraint(name='mass_1', minimum=20, maximum=50)#
    prior['mass_2'] = Constraint(name='mass_2', minimum=20, maximum=50)#
    prior['luminosity_distance'] = PowerLaw(alpha=2, name='luminosity_distance', minimum=200, maximum=700, unit='Mpc', latex_label='$d_L$')#
    prior['phase'] = Uniform(name="phase", minimum=0, maximum=2*np.pi)#
    prior['geocent_time'] = Uniform(name="geocent_time", minimum=time_of_event-0.1, maximum=time_of_event+0.1)#
    prior['a_1'] =  0.0#
    prior['a_2'] =  0.0#
    prior['tilt_1'] =  0.0#
    prior['tilt_2'] =  0.0#
    prior['phi_12'] =  0.0#
    prior['phi_jl'] =  0.0#
    prior['dec'] =  -1.2232#
    prior['ra'] =  2.19432#
    prior['theta_jn'] =  1.89694#
    prior['psi'] =  0.532268#

    #### 额外引入参数
    prior['v_p'] = Uniform(latex_label='$v_p$', name='v_p', minimum=-1e-3, maximum= 1e-3) 

#################################################################################################

    priors = prior
    #################################################################################################################
    logger = bilby.core.utils.logger
    outdir = 'results' + '_' + datetime.datetime.now().strftime('%Y%m%d%H%M') + '/' + label + '_' + str(random.randint(0,100))

    maximum_frequency = 512
    minimum_frequency = 20

    roll_off = 0.4  # Roll off duration of tukey window in seconds, default is 0.4s
    duration = 4  # Analysis segment duration
    post_trigger_duration = 2  # Time between trigger time and end of segment
    end_time = trigger_time + post_trigger_duration
    start_time = end_time - duration

    psd_duration = 32 * duration
    psd_start_time = start_time - psd_duration
    psd_end_time = start_time

    # We now use gwpy to obtain analysis and psd data and create the ifo_list
    ifo_list = bilby.gw.detector.InterferometerList([])
    for det in detectors:
        logger.info("Downloading analysis data for ifo {}".format(det))
        ifo = bilby.gw.detector.get_empty_interferometer(det)
    ###
        data = TimeSeries.fetch_open_data(det, start_time, end_time, cache = True, verbose = True) # 加了缓存，不用反复下载
        ifo.strain_data.set_from_gwpy_timeseries(data)

        logger.info("Downloading psd data for ifo {}".format(det))
        psd_data = TimeSeries.fetch_open_data(det, psd_start_time, psd_end_time, cache = True, verbose = True)
        psd_alpha = 2 * roll_off / duration
        psd = psd_data.psd(
            fftlength=duration, overlap=0, window=("tukey", psd_alpha), method="median"
        )
        ifo.power_spectral_density = bilby.gw.detector.PowerSpectralDensity(
            frequency_array=psd.frequencies.value, psd_array=psd.value
        )
        ifo.maximum_frequency = maximum_frequency
        ifo.minimum_frequency = minimum_frequency
        ifo_list.append(ifo)

    logger.info("Saving data plots to {}".format(outdir))
    bilby.core.utils.check_directory_exists_and_if_not_mkdir(outdir)
    ifo_list.plot_data(outdir=outdir, label=label)

    # In this step we define a `waveform_generator`. This is the object which
    # creates the frequency-domain strain. In this instance, we are using the
    # `lal_binary_black_hole model` source model. We also pass other parameters:
    # the waveform approximant and reference frequency and a parameter conversion
    # which allows us to sample in chirp mass and ratio rather than component mass

    ###波形函数在这里加
    waveform_generator = bilby.gw.WaveformGenerator(
        frequency_domain_source_model=wave_function,
        parameter_conversion=bilby.gw.conversion.convert_to_lal_binary_black_hole_parameters,
        waveform_arguments={
            "waveform_approximant": "IMRPhenomPv2",
            "reference_frequency": 50,
        },
    )

    # In this step, we define the likelihood. Here we use the standard likelihood
    # function, passing it the data and the waveform generator.
    # Note, phase_marginalization is formally invalid with a precessing waveform such as IMRPhenomPv2
    likelihood = bilby.gw.likelihood.GravitationalWaveTransient(
        ifo_list,
        waveform_generator,
        priors=priors,
        time_marginalization=True,
        phase_marginalization=False,
        distance_marginalization=True,
    )

    # Finally, we run the sampler. This function takes the likelihood and prior
    # along with some options for how to do the sampling and how to save the data
    try:
        result = bilby.run_sampler(
            likelihood,
            priors,
            sampler="dynesty",
            outdir=outdir,
            label=label,
            nlive=1000,
            check_point_delta_t=600,
            check_point_plot=True,
            npool=1,
            conversion_function=bilby.gw.conversion.generate_all_bbh_parameters,
        )
        result.plot_corner()

        return 1
    except Exception as e:
        print(e)
        return 0 


if __name__ == "__main__":
    # label = "GW150914" ## 不同事件，改变这里！！！！！！
    # wave_function = lal_binary_black_hole_pv3 #波形函数！！！！！！
    # run(label, wave_function)

    gwBBH = ['GW150914'] * 5

    ta = time.time()

    with Pool() as pool:
        b = pool.map(run, gwBBH)
    print(b)

    tb = time.time()
    print("It costs %.1f s"%(tb-ta))

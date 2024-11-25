#!/usr/bin/env python
"""
Tutorial to demonstrate running parameter estimation on GW150914

This example estimates all 15 parameters of the binary black hole system using
commonly used prior distributions. This will take several hours to run. The
data is obtained using gwpy, see [1] for information on how to access data on
the LIGO Data Grid instead.

[1] https://gwpy.github.io/docs/stable/timeseries/remote-access.html


edited by ysc on 20230822

GW150914, network needed

"""

import sys
sys.path.append("./lib")
from lib.source import lal_binary_black_hole_pv3 #自定义波形函数
                                                         
##################################################################
import bilby
# from bilby.gw.source import lal_binary_black_hole       
import numpy as np
from gwpy.timeseries import TimeSeries
from bilby.core.prior import Uniform, PowerLaw, LogUniform, Constraint, Sine, Cosine
import datetime
from gwosc.datasets import event_gps, event_detectors, find_datasets, run_segment
from gwosc import api
from multiprocessing import Pool
import random 
import time 
import logging
import os
from math import ceil, floor
import pandas as pd
##需要修改的地方##############################################################################################################

def run(label):
    #改为自定义函数
    wave_function = lal_binary_black_hole_pv3
    ###
    # merge时间
    if internet_is_OK:
        events = np.array(find_datasets(type='event'))
        eventList = []
        for item in events:
            if item.startswith("GW"):
                eventList.append(item[0:-3])
        eventSet = list(set(eventList)) #去除同一事件不同版本的数据
        eventSet.sort()
        eventSet = np.array(eventSet)
        labelfull = events[np.array([item.startswith(label) for item in events])][-1]
        info = api.fetch_event_json(labelfull)

        trigger_time = event_gps(label)
        detectors = event_detectors(label)

        chirp_mass_source         = info['events'][labelfull]['chirp_mass_source']
        chirp_mass_source_upper   = info['events'][labelfull]['chirp_mass_source_upper']
        chirp_mass_source_lower   = info['events'][labelfull]['chirp_mass_source_lower']
        luminosity_distance       = info['events'][labelfull]['luminosity_distance']
        luminosity_distance_upper = info['events'][labelfull]['luminosity_distance_upper']
        luminosity_distance_lower = info['events'][labelfull]['luminosity_distance_lower']

        mass_1_source             = info['events'][labelfull]['mass_1_source']
        mass_1_source_upper       = info['events'][labelfull]['mass_1_source_upper']
        mass_1_source_lower       = info['events'][labelfull]['mass_1_source_lower']
        mass_2_source             = info['events'][labelfull]['mass_2_source']
        mass_2_source_upper       = info['events'][labelfull]['mass_2_source_upper']
        mass_2_source_lower       = info['events'][labelfull]['mass_2_source_lower']

    else:
        eventinfo = pd.read_csv("./data/events_info.csv")
        trigger_time = eventinfo[eventinfo['event'] == label]['event_GPS'].values[0]
        detectors = eventinfo[eventinfo['event'] == label]['event_detector'].values[0].split(' ')
        chirp_mass_source         = eventinfo[eventinfo['event'] == label]['chirp_mass_source'].values[0]
        chirp_mass_source_upper   = eventinfo[eventinfo['event'] == label]['chirp_mass_source_upper'].values[0]
        chirp_mass_source_lower   = eventinfo[eventinfo['event'] == label]['chirp_mass_source_lower'].values[0]
        luminosity_distance       = eventinfo[eventinfo['event'] == label]['luminosity_distance'].values[0]
        luminosity_distance_upper = eventinfo[eventinfo['event'] == label]['luminosity_distance_upper'].values[0]
        luminosity_distance_lower = eventinfo[eventinfo['event'] == label]['luminosity_distance_lower'].values[0]
        mass_1_source             = eventinfo[eventinfo['event'] == label]['mass_1_source'].values[0]
        mass_1_source_upper       = eventinfo[eventinfo['event'] == label]['mass_1_source_upper'].values[0]
        mass_1_source_lower       = eventinfo[eventinfo['event'] == label]['mass_1_source_lower'].values[0]
        mass_2_source             = eventinfo[eventinfo['event'] == label]['mass_2_source'].values[0]
        mass_2_source_upper       = eventinfo[eventinfo['event'] == label]['mass_2_source_upper'].values[0]
        mass_2_source_lower       = eventinfo[eventinfo['event'] == label]['mass_2_source_lower'].values[0]


    chirp_mass_source_max = ceil(chirp_mass_source + 5/4 * chirp_mass_source_upper)
    chirp_mass_source_min = floor(chirp_mass_source + 5/4 * chirp_mass_source_lower)

    luminosity_distance_max = ceil(luminosity_distance + 5/4 * luminosity_distance_upper)
    luminosity_distance_min = floor(luminosity_distance + 5/4 * luminosity_distance_lower)

    # mass_ratio_max = round((mass_2_source + mass_2_source_upper) /(mass_1_source + mass_1_source_lower),2)
    # print(mass_ratio_max)
    mass_ratio_min = round((mass_2_source + mass_2_source_lower) /(mass_1_source + mass_1_source_upper),3)


    ## 改变prior 导入方式
    ##priors = bilby.gw.prior.BBHPriorDict(filename="GW150914.prior")

    ### 15 
    priors = bilby.core.prior.PriorDict()
    priors['chirp_mass']          = Uniform(name='chirp_mass', minimum=chirp_mass_source_min, maximum=chirp_mass_source_max, unit='$M_{\odot}$')
    priors['mass_ratio']          = Uniform(name='mass_ratio', minimum=mass_ratio_min, maximum=1)                    
    priors['mass_1']              = Constraint(name='mass_1', minimum=10, maximum=80)                                          
    priors['mass_2']              = Constraint(name='mass_2', minimum=10, maximum=80)                                          
    priors['a_1']                 = Uniform(name='a_1', minimum=0, maximum=0.8, boundary='reflective')                        
    priors['a_2']                 = Uniform(name='a_2', minimum=0, maximum=0.8, boundary='reflective')                         
    priors['tilt_1']              = Sine(name='tilt_1', boundary='reflective')
    priors['tilt_2']              = Sine(name='tilt_2', boundary='reflective')
    priors['phi_12']              = Uniform(name='phi_12', minimum=0, maximum=2 * np.pi, boundary='periodic')
    priors['phi_jl']              = Uniform(name='phi_jl', minimum=0, maximum=2 * np.pi, boundary='periodic')
    priors['luminosity_distance'] = PowerLaw(alpha=2, name='luminosity_distance', minimum=luminosity_distance_min, maximum=luminosity_distance_max, unit='Mpc', latex_label='$d_L$') 
    priors['dec']                 = Cosine(name='dec')
    priors['ra']                  = Uniform(name='ra', minimum=0, maximum=2 * np.pi, boundary='periodic') 
    priors['theta_jn']            = Sine(name='theta_jn')
    priors['psi']                 = Uniform(name='psi', minimum=0, maximum=np.pi, boundary='periodic') 
    priors['phase']               = Uniform(name='phase', minimum=0, maximum=2 * np.pi, boundary='periodic') 
    priors['geocent_time']        = Uniform(name="geocent_time", minimum=trigger_time - 0.1, maximum=trigger_time + 0.1)

    #### 额外引入参数
    priors['v_p'] = Uniform(latex_label='$v_p$', name='v_p', minimum=-1e-3, maximum= 1e-3) 

    #################################################################################################################
    logger = bilby.core.utils.logger
    outdir1 = 'results' + '_' + datetime.datetime.now().strftime('%Y%m%d%H%M') #outer dir
    outdir2 = '/' + label + '_' + str(random.randint(0,100))                   #inter/event dir
    outdir = outdir1 + outdir2

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

    ######log############################################################################################################
    if not os.path.exists(outdir1):   # make dir
        os.system("mkdir " + outdir1)
    os.system("mkdir " + outdir)
    logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', filename= outdir + '/' + 'run.log', level=logging.INFO) 
    ######log############################################################################################################


    # We now use gwpy to obtain analysis and psd data and create the ifo_list
    ifo_list = bilby.gw.detector.InterferometerList([])
    for det in detectors:

        ifo = bilby.gw.detector.get_empty_interferometer(det)
    ###
        try:
            
            if internet_is_OK:
                ###download data#####################################################################################################
                data = TimeSeries.fetch_open_data(det, start_time, end_time, cache = True, verbose = True) # 加了缓存，不用反复下载

                logger.info("Downloading analysis data for ifo {}".format(det))
                logging.info("Downloading analysis data for ifo {}".format(det))

                psd_data = TimeSeries.fetch_open_data(det, psd_start_time, psd_end_time, cache = True, verbose = True)

                logger.info("Downloading psd data for ifo {}".format(det))
                logging.info("Downloading psd data for ifo {}".format(det))
                ###download data#####################################################################################################
            else:
                if os.path.exists('./data/'+label):
                    start_str = str(int(ceil(trigger_time) - 4096 / 2))
                    filename = det[0] + '-' + det + '_GWOSC_4KHZ_R1-' + start_str + '-4096.gwf'
                    data0 = TimeSeries.read('./data/'+ label + '/' + filename, det + ":GWOSC-4KHZ_R1_STRAIN") #downloaded data 4096s
                    data_sample_rate = 4096
                    index1 = int((data_sample_rate - duration)/ 2 * data_sample_rate)              #analysis data start index
                    index2 = int(index1 + duration * data_sample_rate)                             #analysis data end index
                    index0 =  int(index1 - psd_duration * data_sample_rate)                        #psd data start index

                    data = data0[index1:index2]
                    logger.info("Reading analysis data for ifo {}".format(det))
                    logging.info("Reading analysis data for ifo {}".format(det))

                    psd_data = data0[index0:index1]
                    logger.info("Reading psd data for ifo {}".format(det))
                    logging.info("Reading psd data for ifo {}".format(det))
                else:
                    raise Exception("GW data not found, please download GW data first!")

        except Exception as e:
            logging.info(e)
            raise Exception

        ifo.strain_data.set_from_gwpy_timeseries(data)
    
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
    logging.info("Saving data plots to {}".format(outdir))

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
            "reference_frequency": 20,
        },
    )

    # In this step, we define the likelihood. Here we use the standard likelihood
    # function, passing it the data and the waveform generator.
    # Note, phase_marginalization is formally invalid with a precessing waveform such as IMRPhenomPv2
    likelihood = bilby.gw.likelihood.GravitationalWaveTransient(
        ifo_list,
        waveform_generator,
        priors=priors,
        time_marginalization=False,
        phase_marginalization=False,
        distance_marginalization=False,
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
            nact=50,
        )
        result.plot_corner()

        return 1
    except Exception as e:
        logging.info(e)
        return 0 


if __name__ == "__main__":

    internet_is_OK_input = "N" # Y or N means internet is OK or not OK 

    if internet_is_OK_input == "Y" or internet_is_OK_input == "y":
        internet_is_OK = True
    else:
        internet_is_OK = False

    gwBBH = ['GW200129_065458', 'GW150914', 'GW190521', 'GW190814']*2 

    ta = time.time()

    with Pool() as pool:
        b = pool.map(run, gwBBH)
    print(b)

    tb = time.time()
    print("It costs %.1f s"%(tb-ta))

from abc import ABCMeta, abstractmethod
from gwosc.datasets import find_datasets, run_segment, event_detectors, event_gps
from gwosc.locate import get_run_urls, get_event_urls
from gwosc import api
from json.decoder import JSONDecodeError
import logging
from multiprocessing import Pool
import os
import re
import pandas as pd
import numpy as np

class abstractGetData(metaclass=ABCMeta):
    """下载数据的抽象类"""
    def __init__(self, datasets, dirname = None):
        """初始化，创建下载文件夹，文件夹名称若为空，则默认为数据库名称database"""
        self.datasets = datasets
        
        if dirname:
            self.dirname  = dirname
        else:
            self.dirname = datasets

        if not os.path.exists(self.dirname):
            os.system("mkdir " + self.dirname)
        
        logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', filename='download.log', level=logging.INFO) 
        logging.info("Created Directory " + self.dirname)

    def __down__(self, url):
        """根据网址下载数据"""
        try:
            os.system("wget -P " + self.dirname + '/ --no-check-certificate '+ url)
            logging.info("Dowloaded form " + url)
            return 1
        except ValueError as e:
            logging.error(e)

    @abstractmethod
    def download(self):
        pass

class getEvent(abstractGetData):
    """下载事件数据，继承自AbstractGetdata"""
    def __init__(self, datasets, dirname = None):
        super().__init__(datasets, dirname)
        
    def __downWhichDetector__(self, detector):
        """某次引力波事件某一探测器的全部数据，并行"""
        try:
            urls = get_event_urls(self.datasets, sample_rate=self.sample_rate, format = self.format)
            #检查某一数据段是否已下载，删除重复网址
            
            if self.format == "txt":
                pattern = re.compile(detector[0] + '-.*.-'+ str(self.duration) + "." +  self.format + ".gz")
            else:
                pattern = re.compile(detector[0] + '-.*.-'+ str(self.duration) + "." +  self.format)

            urls_reduced = []
            for url in urls:   
                try:
                    if not os.path.exists(self.dirname + '/' + pattern.search(url).group()): #如果未下载，则加入精简url列表
                        urls_reduced.append(url)
                except AttributeError:
                    pass    

            if urls_reduced:                  #如果urls_reduced非空，则下载
                self.__down__(urls_reduced[0])

        except JSONDecodeError:
            logging.info(detector + " data not exits in " + self.datasets)

    def download(self, duration=32, sample_rate=4096, format_="gwf"):
        """下载某次引力波事件所有探测器的全部数据, 
        duration为32或4096秒，
        sample_rate为4096Hz 或者 16384Hz
        """
        self.duration = duration
        self.sample_rate = sample_rate
        self.format = format_

        detectorList = event_detectors(self.datasets)  #self.datasets is event name

        with Pool() as pool:
            pool.map(self.__downWhichDetector__, detectorList)  #并行下载




if __name__ == '__main__':

    outdir = 'data'
    if not os.path.exists(outdir):   # make dir
        os.system("mkdir " + outdir)


    if_update_event_input = input("Update event info? (Y/N) ")  # Y or y for YES, other for NO

    if if_update_event_input == "Y" or if_update_event_input == "y":
        if_update_event = True
    else:
        if_update_event = False

    if if_update_event:
        events = np.array(find_datasets(type='event')) #寻找引力波事件数据，一个事件可能有多个版本
        #得到现有的引力波事件列表
        eventList = []
        for item in events:
            if item.startswith("GW"):
                eventList.append(item[0:-3])
        eventSet = list(set(eventList)) #去除同一事件不同版本的数据
        eventSet.sort()
        eventSet = np.array(eventSet)

        #save GW info
        datainfo = []
        event_set_OK = []
        for item in eventSet:
            try:
                itemfull = events[np.array([item0.startswith(item) for item0 in events])][-1]
                print(itemfull)

                info = api.fetch_event_json(itemfull)
                datainfo.append([item, event_gps(item), " ".join(list(event_detectors(item))),  \
                                 info['events'][itemfull]['chirp_mass_source'], \
                                 info['events'][itemfull]['chirp_mass_source_upper'],\
                                 info['events'][itemfull]['chirp_mass_source_lower'],\
                                 info['events'][itemfull]['luminosity_distance'],\
                                 info['events'][itemfull]['luminosity_distance_upper'],\
                                 info['events'][itemfull]['luminosity_distance_lower'],\
                                 info['events'][itemfull]['mass_1_source'],\
                                 info['events'][itemfull]['mass_1_source_upper'],\
                                 info['events'][itemfull]['mass_1_source_lower'],\
                                 info['events'][itemfull]['mass_2_source'],\
                                 info['events'][itemfull]['mass_2_source_upper'],\
                                 info['events'][itemfull]['mass_2_source_lower'],\
                                 info['events'][itemfull]['network_matched_filter_snr'],\
                                 info['events'][itemfull]['network_matched_filter_snr_upper'],\
                                 info['events'][itemfull]['network_matched_filter_snr_lower'],\
                                 info['events'][itemfull]['p_astro'],\
                                ])
                event_set_OK.append(item)
            except Exception as e:
                print(e)
                

        eventinfo = pd.DataFrame(np.array(datainfo), index = range(0, len(event_set_OK)), columns = [ 'event', 'event_GPS', 'event_detector', 
                                                                                                     'chirp_mass_source',
                                                                                                     'chirp_mass_source_upper',
                                                                                                     'chirp_mass_source_lower',
                                                                                                     'luminosity_distance',
                                                                                                     'luminosity_distance_upper',
                                                                                                     'luminosity_distance_lower',
                                                                                                     'mass_1_source',
                                                                                                     'mass_1_source_upper',
                                                                                                     'mass_1_source_lower',
                                                                                                     'mass_2_source',
                                                                                                     'mass_2_source_upper',
                                                                                                     'mass_2_source_lower',
                                                                                                     'network_matched_filter_snr',
                                                                                                     'network_matched_filter_snr_upper',
                                                                                                     'network_matched_filter_snr_lower',
                                                                                                     'p_astro',
                                                                                                    ])

        eventinfo.to_csv("./data/events_info.csv", mode="w")

    else:
        pass


    if_download_input = input("Download event data? (Y/N) ")  # Y or y for YES, other for NO

    if if_download_input == "Y" or if_download_input == "y":
        if_download = True
    else:
        if_download = False


    if if_download:
        event = "GW" + input("download event data?(eg. GW150914, input 150914)") #eg.'GW150914'

        try:
            test = getEvent(event, dirname = 'data/' + event)
            # test.download(duration=32, sample_rate=4096, format_="gwf") # not necessary
            test.download(duration=4096, sample_rate=4096, format_="gwf")
        except Exception as e:
            logging.error(e)

    else:
        pass



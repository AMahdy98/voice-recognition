from scipy import signal
import json
import librosa as l
from numpy import ndarray

class spectrogram():
    """
    Responsible for creating spectrograms for any .wav file
    implements the following:
    - reads a loaded wav file data and creates the associated spectrum
    - save the spectrum created in an arbitrary file
    """
    def __init__(self):
        """
        Class Initializer

        Parameters
        -----------
        - sampleFreqs : holds the sampled frequencies
        - sampleTime : holds the sampled time rates
        - colorMesh : holds the value (intenisty) of the frequency component
        - container : a dictionary used in the saved process
        """
        print("Initializing Spectrogram")
        self.sampleFreqs = None
        self.sampleTime = None
        self.colorMesh = None
        self.features = None
        self.container = None

    def __call__(self, songData: "numpy.ndarray", songSR: int, window:str, fileName:str,
                 path:str = None, compressed: bool = False, featureize:bool = False):
        """
        Caller function for the class which maintains all it's implemented methods

        Parameters
        -----------
        - songData: a numpy array of the read wav file
        - songSR : integer representing the sample rate
        - window : a str specifying the widow type used in creating the spectrogram
        - path : str if specified the file is saved in the given path
        - fileName : if provided the spectrogram will be saved as a json file
        - compressed : if True only the color mesh will be saved
        - featurize : if True spectrogram`s main features will be extracted and saved if specified saving
        """
        self._spectrogram(songData, songSR, window)
        if featureize:
            self.features= self._spectralFeatures(None, self.colorMesh, songSR,window)
        print("spectrogram created")

        if fileName:
            if path is None:
                self._saveFormat('', fileName, compressed=compressed, featurize=featureize)
                print("saved in main directory .. ")
            else:
                self._saveFormat(path, fileName, compressed=compressed, featurize=featureize)
            print("spectrogram saved")

    def _spectrogram(self, songData: "numpy.ndarray", songSampleRate:int, windowType: str):
        """
        Creates a Spectrogram of the given data

        Parameters
        -----------
        - songData : a numpy array of the read wav file
        - songSampleRate : integer representing the sample rate
        - windowType : a str specifying the widow type used in creating the spectrogram
        """
        if len(songData.shape) == 2:
            print("song is stereo")
            print("Converting ..")
            self.sampleFreqs, self.sampleTime, self.colorMesh = signal.spectrogram(songData[:, 0],
                                                                                   fs=songSampleRate, window=windowType)
        else:
            self.sampleFreqs, self.sampleTime, self.colorMesh = signal.spectrogram(songData,
                                                                                   fs=songSampleRate, window=windowType)

    def _saveFormat(self, folder:str, filename:str, featurize : bool = False, compressed: bool = False):
        """
        Save the spectrum in a specified filename.json

        Parameters
        -----------
        - folder : a path to the file location
        - filename : the file name
        - compressed : if True only the color mesh will be saved
        - featurize : if True adds the main features of the spectrogram
        """
        # TODO : Refactor this part .. return function
        if compressed:
            self.container = {"color_mesh": self.colorMesh.tolist()}
        else:
            self.container = {'sample_frequencies': self.sampleFreqs.tolist(),
                              "sample_time": self.sampleTime.tolist(),
                              "color_mesh": self.colorMesh.tolist()}
        if featurize:
            self.container['features'] = self.features

        with open(folder+filename+".json", 'w') as outfile:
            json.dump(self.container, outfile)

    def _spectralFeatures(self, song: "np.ndarray"= None, S: "np.ndarray" = None, sr: int = 22050, window:'str'='hann'):
        """
        Calculates the Spectral Centroid of a given data or the data instantiated in the class
        Parameters
        -----------
        - song  : wav file array
        - S    : spectrogram readings
        - sr : sampling frequency default 22050
        - window: a string specifying the window applied default hann (see options)

        Options
        -------
        - boxcar
        - triang
        - blackman
        - hamming
        - hann
        - bartlett
        - flattop
        - parzen
        - bohman
        - blackmanharris
        - nuttall
        - barthann
        - kaiser (needs beta)
        - gaussian (needs standard deviation)
        - general_gaussian (needs power, width)
        - slepian (needs width)
        - dpss (needs normalized half-bandwidth)
        - chebwin (needs attenuation)
        - exponential (needs decay scale)
        - tukey (needs taper fraction)
        """
        if not (song or sr) :
            print('provide either a wav file data or a spectrogram readings or both')
        else:
            return ndarray(l.feature.spectral_centroid(y= song, sr=sr, S=S,window = window),
                           l.feature.spectral_rolloff(y= song, sr=sr, S=S,window = window),
                           l.feature.melspectrogram(y= song, sr=sr, S=S,window = window))

if __name__ == '__main__':
    # Basic Usage

    from scipy.io import wavfile
    sampleRate, songdata = wavfile.read("tests/Adele_Million_Years_Ago_10.wav")
    spectrum = spectrogram()
    # spectrum(songdata, sampleRate, window='hann', songName="test", compressed=True, path='tests/')
    spectrogram()._spectralCentroid()



import MidiPlayer from "midi-player-js";
import { SplendidGrandPiano, Soundfont, Sampler } from "smplr";

export default class {
  private midiPlayer:MidiPlayer.Player;
  private instrument:Sampler;

  constructor(){
    
    this.midiPlayer = new MidiPlayer.Player((event:any) => {});

    const context = new AudioContext();
    this.instrument = new SplendidGrandPiano(context);

    this.midiPlayer.on("playing", this.onPlayingCallback);
    this.midiPlayer.on("midiEvent", this.onMidiEventCallback);
    this.midiPlayer.on("endOfFile", this.onFinishCallback);
  }

  public load = (buffer: ArrayBuffer ) => {
    return new Promise(async (resolve, reject) => {
      this.midiPlayer.loadArrayBuffer(buffer);
      await this.instrument.loaded();
      resolve(null);
      console.log("loaded");
    });
    
  }

  public play = () => {
    this.midiPlayer.play();
    console.log("MIDI started playing");
  }

  public stopPlaying = () => {
    if(this.midiPlayer.isPlaying()){
      this.midiPlayer.stop();
    }
  }


  private onPlayingCallback = (e:any) => {
  }

  private onMidiEventCallback = (e:any) => {
    console.log("onMidiEventCallback", e);
    switch(e.name){
      case "Note on":
        this.instrument.start(e.noteName);
        break;
      case "Note off":
        this.instrument.stop(e.noteName);
        break;
      default:
        break;
    }
  }

  private onFinishCallback = (e:any) => {
    console.log("onFinishCallback", e)
  }

}
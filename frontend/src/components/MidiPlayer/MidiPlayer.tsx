import React, { useEffect, useState } from 'react'
import MidiService from '../../services/MidiService'
import { Button, HStack } from '@chakra-ui/react'

export default function MidiPlayer() {
  const MIDI_URL = process.env.PUBLIC_URL + "/test.mid";
  const [loading, setLoading] = useState<boolean>(true);
  const [player, setPlayer] = useState<MidiService|undefined>(undefined);

  useEffect(() => {
    const fetchMIDI = async () => {
      const midiService = new MidiService();
      const res = await fetch(MIDI_URL);
      const buffer = await res.arrayBuffer();
      await midiService.load(buffer);
      setPlayer(midiService);
      setLoading(false);
    }
    fetchMIDI();
  }, []);

  const onPlayCallback = async (e:React.MouseEvent) => {
    if(!player) return;
    player.play();
  }

  const onStopCallback = (e:React.MouseEvent) => {
    if(!player) return;
    player.stopPlaying();
  }

  return (
    <div>
      {loading 
      ? <p>Loading...</p>
      : (<HStack>
          <Button onClick={(e) => onPlayCallback(e)}>Play</Button>
          <Button onClick={(e) => onStopCallback(e)}>Stop</Button>
        </HStack>)
      }
    </div>
  )
}

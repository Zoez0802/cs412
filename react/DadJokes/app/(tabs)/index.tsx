// app/(tabs)/index.tsx
// Author: Minjie Zuo (minjiez@bu.edu), 3/28/2026
// This file defines the index screen for the DadJokes application.
import { useEffect, useState } from 'react';
import { Image } from 'react-native';
import { Text, View } from '@/components/Themed';
import { styles } from '../../assets/my_styles';

export default function IndexScreen() {
  'This is the index screen for the app. It shows one random joke and one random picture from the API.';
  //store joke and picture
  const [joke, setJoke] = useState<any>([]); 
  const [pic, setPic] = useState<any>([]);

  // get data from Django API
  async function getData() {
    'This function sends two GET requests to the Django API to get one random joke and one random picture, and stores them in state'
    const jokeRes = await fetch('https://cs-webapps.bu.edu/minjiez/dadjokes/api/random');
    const jokeData = await jokeRes.json();

    const picRes = await fetch('https://cs-webapps.bu.edu/minjiez/dadjokes/api/random_picture');
    const picData = await picRes.json();

    setJoke(jokeData);
    setPic(picData);
  }

  //this is an extra function to format the timestamp string from API to a more readable format
  function showTime(time: string) {
    const d = new Date(time);

    return d.toLocaleString([], {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: 'numeric',
      minute: '2-digit',
    });
  }

  // run once when screen loads
  useEffect(() => {
    getData();
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.titleText}>Dad Jokes</Text>

      <View style={styles.box}>
        <Text style={styles.jokeText}>{joke.text}</Text>

        <Text style={styles.infoText}>
          {joke.contributor} · {showTime(joke.created_at)}
        </Text>

        <Image
          source={{ uri: pic.image_url }}
          style={styles.image}
        />
      </View>
    </View>
  );
}
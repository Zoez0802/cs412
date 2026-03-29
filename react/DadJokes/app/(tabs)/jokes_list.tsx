// jokes_list.tsx
// Author: Minjie Zuo (minjiez@bu.edu), 3/29/2026
// This screen shows a list of jokes from the API.

import { useEffect, useState } from 'react';
import { FlatList } from 'react-native';
import { Text, View } from '@/components/Themed';
import { styles } from '../../assets/my_styles';

export default function JokeListScreen() {
  // store all jokes
  const [jokes, setJokes] = useState<
    { id: number; text: string; contributor: string; created_at: string }[]
  >([]);

  // get all jokes from the API
  async function getJokes() {
    try {
      const res = await fetch(
        'https://cs-webapps.bu.edu/minjiez/dadjokes/api/jokes'
      );
      const data = await res.json();

      console.log('jokes data:', data);
      setJokes(data.results);
    } catch (error) {
      console.log('Could not get jokes:', error);
    }
  }

  // my extra function tomake the time easier to read
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

  // load jokes when the screen opens
  useEffect(() => {
    getJokes();
  }, []);

  return (
    <View>
      <Text style={styles.titleText}>All Jokes</Text>

      <FlatList
        data={jokes}
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item }) => (
          <View style={styles.box}>
            <Text style={styles.jokeText}>{item.text}</Text>
            <Text style={styles.infoText}>
              {item.contributor} · {showTime(item.created_at)}
            </Text>
          </View>
        )}
      />
    </View>
  );
}
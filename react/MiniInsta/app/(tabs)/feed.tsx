// app/(tabs)/feed.tsx
// Author: Minjie Zuo , 4/6/2026
// This screen shows the feed (posts from followed users) for one profile. It fetches the feed data from the backend and displays each post's caption, timestamp, and first photo (if available) in a list format. The styles are imported from the shared styles file to maintain a consistent look across the app.
import { useEffect, useState } from 'react';
import { View, Text, FlatList, Image } from 'react-native';
import { styles } from '../../assets/my_styles';

export default function FeedScreen() {
  const BASE_URL = 'https://cs-webapps.bu.edu/minjiez/mini_insta';

  const [posts, setPosts] = useState<any[]>([]);
  const [message, setMessage] = useState('');

  //Load the feed posts for the logged-in user.
  async function loadFeed() {
    const token = (globalThis as any).token;
    const profileId = (globalThis as any).profileId;

    if (!token || !profileId) {
      console.log('No login token or profile id yet.');
      return;
    }

    try {
      const res = await fetch(
        `${BASE_URL}/api/profile/${profileId}/feed?token=${token}`
      );

      console.log('feed status:', res.status);
      
      const text = await res.text();
      if (!res.ok) {
        setMessage('Could not load feed :(');
        return;
      }

      const data = JSON.parse(text);
      console.log('feed data:', data);

      if (data.results) {
        setPosts(data.results);
      } else if (Array.isArray(data)) {
        setPosts(data);
      } else {
        setPosts([]);
      }
    } catch (error) {
      console.log('Feed error:', error);
      setMessage('Something went wrong :(');
    }
  }

useEffect(() => {
  loadFeed();
}, []);

  function renderItem({ item }: { item: any }) {
    let image_url = '';

    if (item.photos && item.photos.length > 0) {
      image_url = item.photos[0].image;

      if (image_url.startsWith('/')) {
        image_url = `https://cs-webapps.bu.edu${image_url}`;
      }
    }

    return (
      <View style={styles.box}>
        <Text>@{item.profile?.username}</Text>

        <Text style={styles.postText}>
          {item.caption ? item.caption : 'No caption'}
        </Text>

        <Text style={styles.infoText}>{item.timestamp}</Text>

        {image_url ? (
          <Image source={{ uri: image_url }} style={styles.image} />
        ) : null}
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <Text style={styles.titleText}>Feed</Text>

      {message ? <Text style={styles.smallText}>{message}</Text> : null}

      <FlatList
        data={posts}
        renderItem={renderItem}
        keyExtractor={(item) => item.id.toString()}
      />
    </View>
  );
}
// app/(tabs)/index.tsx
// Author: Minjie Zuo
// This screen shows one profile and that profile's posts.

////useCallback: to reload the profile and posts when the user comes back to this screen after creating a new post. 
import { useEffect, useState, useCallback } from 'react';
import { View, Text, FlatList, Image } from 'react-native';
import { styles } from '../../assets/my_styles';
//run the callback function every time the screen is focused, 
// which means every time the user comes back to this screen, 
// it will reload the profile and posts. 
import { useFocusEffect } from '@react-navigation/native';

// Define TypeScript types for the data structures used in the profile and posts.
type PhotoType = {
  id: number;
  image: string;
};

type ProfileType = {
  id: number;
  display_name: string;
  username: string;
  bio_text: string | null;
  profile_image_url?: string;
};

type PostType = {
  id: number;
  caption: string;
  timestamp: string;
  photos: PhotoType[];
};

export default function ProfileScreen() {
  const BASE_URL = 'https://cs-webapps.bu.edu/minjiez/mini_insta';

  const [profile, setProfile] = useState<ProfileType | null>(null);
  const [posts, setPosts] = useState<PostType[]>([]);
  const [message, setMessage] = useState('');

  //// Load the profile and that profile's posts.
  async function loadData() {
    const token = (globalThis as any).token;
    const profileId = (globalThis as any).profileId;

    if (!token || !profileId) {
      console.log('No login token or profile id.');
      return;
    }

    try {
      const res1 = await fetch(
        `${BASE_URL}/api/profile/${profileId}?token=${token}`
      );

      console.log('profile status:', res1.status);//debug

      const text1 = await res1.text();
      console.log('profile raw text:', text1);

      if (!res1.ok) {
        setMessage('Can not load profile.');
        return;
      }

      const profileData = JSON.parse(text1);

      const res2 = await fetch(
        `${BASE_URL}/api/profile/${profileId}/posts?token=${token}`
      );


      const text2 = await res2.text();

      if (!res2.ok) {
        setMessage('Could not load posts.');
        return;
      }

      const postData = JSON.parse(text2);

      setProfile(profileData);

      if (postData.results) {
        setPosts(postData.results);
      } else if (Array.isArray(postData)) {
        setPosts(postData);
      } else {
        setPosts([]);
      }
    } catch (err) {
      console.log('Error loading profile:', err);
      setMessage('Something went wrong ;(');
    }
  }

  useEffect(() => {
    loadData();
  }, []);

  // Reload when the user comes back to this screen.
  useFocusEffect(
    useCallback(() => {
      loadData();

      if ((globalThis as any).postChanged) {
        loadData();
        (globalThis as any).postChanged = false;
      }
    }, [])
  );


  function renderPost({ item }: { item: PostType }) {
    let image_url = '';

    if (item.photos && item.photos.length > 0) {
      image_url = item.photos[0].image;

      if (image_url.startsWith('/')) {
        image_url = `https://cs-webapps.bu.edu${image_url}`;
      }
    }

    return (
      <View style={styles.box}>
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
      <Text style={styles.titleText}>My Profile</Text>

      {message ? <Text style={styles.smallText}>{message}</Text> : null}

      {profile ? (
        <View style={styles.box}>
          <Text style={styles.nameText}>{profile.display_name}</Text>
          <Text style={styles.handleText}>@{profile.username}</Text>

          {profile.bio_text ? (
            <Text style={styles.bioText}>{profile.bio_text}</Text>
          ) : null}

          {profile.profile_image_url ? (
            <Image
              source={{ uri: profile.profile_image_url }}
              style={styles.image}
            />
          ) : null}
        </View>
      ) : (
        <Text>I AM SLOWLY LOADING ...</Text>
      )}

      <Text style={styles.sectionTitle}>My Posts</Text>

      <FlatList
        data={posts}
        renderItem={renderPost}
        keyExtractor={(item) => item.id.toString()}
      />
    </View>
  );
}
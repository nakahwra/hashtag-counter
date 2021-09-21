import TwitterStreamChannels from 'twitter-stream-channels';
import { getConnection } from './services/db';

async function streamConnect() { 
  const dbClient = await getConnection();

  const db = dbClient.db('hashtag_counter')
  return db.collection("tweets");
}

export async function getStream() {
  const credentials = require('../credentials.json')

  const channels = {
    "languages" : [
      '#java ',
      '#javascript',
      '#python',
      '#html',
      '#css',
      '#php',
      '#ruby',
      '#kotlin',
      '#flutter',
      '#perl',
      '#assembly',
      '#swift',
      '#sql',
      '#rust',
      '#haskell',
      '#lisp',
      '#elixir',
    ],
  };

  const collection = await streamConnect();
  
  const client = new TwitterStreamChannels(credentials);
  const stream = client.streamChannels({track:channels});

  stream.on('channels/languages', async function(tweet){
    if (!tweet.retweeted_status && !tweet.is_quote_status) {
      tweet.$keywords = tweet.$keywords.map((keyword: string) => keyword.trim())

      const newTweet = {
        text: tweet.text,
        keywords: tweet.$keywords,
      }
  
      await collection.insertOne(newTweet)
      console.log(newTweet);
    }
  });
}
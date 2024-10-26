import opentimelineio as otio

class VideoTimelineResolveOTIO:
    def __init__(self, frame_rate=60, resolution=(1920, 1080)):
        self.clips = []
        self.frame_rate = frame_rate
        self.resolution = resolution

        # Create the timeline and tracks
        self.timeline = otio.schema.Timeline(name="VideoSequence")
        self.video_track = otio.schema.Track(kind=otio.schema.TrackKind.Video, name="VideoTrack")
        self.audio_track1 = otio.schema.Track(kind=otio.schema.TrackKind.Audio, name="AudioTrack1")
        self.audio_track2 = otio.schema.Track(kind=otio.schema.TrackKind.Audio, name="AudioTrack2")

        self.timeline.tracks.append(self.video_track)
        self.timeline.tracks.append(self.audio_track1)
        self.timeline.tracks.append(self.audio_track2)

    def add_clip(self, filepath, start_time, duration):
        """Add a reference to a video clip to the timeline."""
        self.clips.append({
            'filepath': filepath,
            'start_time': start_time,
            'duration': duration
        })

    def generate_timeline(self):
        """Generate the timeline using OpenTimelineIO."""
        rate = self.frame_rate
        prev_duration = otio.opentime.RationalTime(0, rate)

        for clip_info in self.clips:
            filepath = clip_info['filepath']
            start_time = clip_info['start_time']
            duration = clip_info['duration']

            # Create media reference for video
            video_media_ref = otio.schema.ExternalReference(
                target_url=filepath
            )

            # Create media reference for audio
            audio_media_ref = otio.schema.ExternalReference(
                target_url=filepath
            )

            # Create the video clip with source range
            video_clip = otio.schema.Clip(
                name=filepath.split('/')[-1],
                media_reference=video_media_ref,
                source_range=otio.opentime.TimeRange(
                    start_time=otio.opentime.RationalTime(start_time * rate, rate),
                    duration=otio.opentime.RationalTime(duration * rate, rate)
                )
            )

            self.video_track.append(video_clip)

            metadata = {
                "Resolve_OTIO": {
                    "Channels": [
                        {
                            "Source Channel ID": 0,  # Left channel
                            "Source Track ID": 0     # Single track ID for both channels
                        },
                        {
                            "Source Channel ID": 1,  # Right channel
                            "Source Track ID": 0     # Single track ID for both channels
                        }
                    ]
                    # "Link Group ID": 1 
                }
            }

            # Create the audio clip with the same source range
            audio_clip = otio.schema.Clip(
                name=filepath.split('/')[-1] + " (Audio)",
                media_reference=audio_media_ref, metadata=metadata,
                source_range=otio.opentime.TimeRange(
                    start_time=otio.opentime.RationalTime(start_time * rate, rate),
                    duration=otio.opentime.RationalTime(duration * rate, rate)
                )
            )

            self.audio_track1.append(audio_clip)
            metadata = {
                "Resolve_OTIO": {
                    "Channels": [
                        {
                            "Source Channel ID": 0,  # Left channel
                            "Source Track ID": 1     # Single track ID for both channels
                        },
                        {
                            "Source Channel ID": 1,  # Right channel
                            "Source Track ID": 1     # Single track ID for both channels
                        }
                    ]
                    # "Link Group ID": 1  # Grouping the audio channels to one clip
                }
            }

            # Create the audio clip with the same source range
            audio_clip = otio.schema.Clip(
                name=filepath.split('/')[-1] + " (Audio)",
                media_reference=audio_media_ref, metadata=metadata,
                source_range=otio.opentime.TimeRange(
                    start_time=otio.opentime.RationalTime(start_time * rate, rate),
                    duration=otio.opentime.RationalTime(duration * rate, rate)
                )
            )

            self.audio_track2.append(audio_clip)


            prev_duration += video_clip.source_range.duration

    def write_to_file(self, output_filepath):
        """Write the timeline to a file in FCPXML format."""
        self.generate_timeline()
        otio.adapters.write_to_file(self.timeline, output_filepath)

# Usage Example
# timeline = VideoTimelineResolveOTIO()
# timeline.add_clip("podcast.mkv", start_time=0, duration=10)   # Reference first 10 seconds
# timeline.add_clip("podcast.mkv", start_time=10, duration=5)   # Reference next 5 seconds
# timeline.write_to_file("testotio.otio")

# Design Document (設計書)

## Table schema

* User
    id (主キー)
    nickname (名前)
    username (ユーザー名)
    password (パスワード)
    email (メールアドレス)
    avatar (プロフィール画像)
    header (プロフィールヘッダー画像)
    description (プロフィールの自己紹介)
    created_at (作成日時)
    updated_at (更新日時)
    locale (言語)
    last_login (最終ログイン日時)
    is_active (アカウントが有効かどうか)
    is_staff (スタッフかどうか)
    is_superuser (スーパーユーザーかどうか)
* Following
    id (主キー)
    user_id (外部キー)
    following_user_id (外部キー)
    created_at (作成日時)
    updated_at (更新日時)
* Followers
    id (主キー)
    user_id (外部キー)
    follower_user_id (外部キー)
    created_at (作成日時)
    updated_at (更新日時)
* Friends
    id (主キー)
    user_id (外部キー)
    friend_user_id (外部キー)
    created_at (作成日時)
    updated_at (更新日時)
* FriendRequest
    id (主キー)
    from_user_id (外部キー)
    to_user_id (外部キー)
    status (文字列)
    created_at (作成日時)
    updated_at (更新日時)
* Posts
    id (主キー)
    user_id (外部キー)
    title (投稿タイトル)
    content (投稿内容)
    created_at (作成日時)
    updated_at (更新日時)
* PostComments
    id (主キー)
    user_id (外部キー)
    post_id (外部キー)
    content (コメント内容)
    created_at (作成日時)
    updated_at (更新日時)
    parent_comment_id (親コメントのID)
* Playlists
    id (主キー)
    user_id (外部キー)
    name (プレイリスト名)
    created_at (作成日時)
    updated_at (更新日時)
* ProfileComments
    id (主キー)
    user_id (外部キー)
    profile_id (外部キー)
    content (コメント内容)
    created_at (作成日時)
    updated_at (更新日時)
    parent_comment_id (親コメントのID)
* MessageThreads
    id (主キー)
    sender_id (外部キー)
    recipient_id (外部キー)
    title (スレッドタイトル)
    created_at (作成日時)
* Messages
    id (主キー)
    sender_id (外部キー)
    thread_id (外部キー)
    content (メッセージ内容)
    created_at (作成日時)
* Notifications
    id (主キー)
    user_id (外部キー)
    message (通知メッセージ)
    read (既読かどうか)
    created_at (作成日時)
    updated_at (更新日時)
* NotificationSettings
    id (主キー)
    user_id (外部キー)
    mension_enabled (メンション通知設定)
    comment_enabled (コメント通知設定)
    reply_enabled (返信通知設定)
    created_at (作成日時)
    updated_at (更新日時)
* BlacklistTags
    id (主キー)
    user_id (外部キー)
    tag_id (外部キー)
    created_at (作成日時)
* Polls
    id (主キー)
    user_id (外部キー)
    question (投票質問)
    created_at (作成日時)
    updated_at (更新日時)
* PollOptions
    id (主キー)
    poll_id (外部キー)
    option_text (オプションのテキスト)
    created_at (作成日時)
    updated_at (更新日時)
* PollResponses
    id (主キー)
    user_id (外部キー)
    poll_id (外部キー)
    option_id (外部キー)
    created_at (作成日時)
* Videos
    id (主キー)
    title (動画タイトル)
    description (動画説明)
    user_id (外部キー)
    video_file (動画ファイル)
    video_url (動画のURL)
    thumbnail (動画サムネイル)
    rating (動画の類型)
    views_count (ビュー数)
    likes_count (ライク数)
    created_at (作成日時)
    updated_at (更新日時)
* VideoComments
    id (主キー)
    user_id (外部キー)
    video_id (外部キー)
    content (コメント内容)
    created_at (作成日時)
    updated_at (更新日時)
    parent_comment_id (親コメントのID)
* VideoLikes
    id (主キー)
    user_id (外部キー)
    video_id (外部キー)
    created_at (作成日時)
* ImageSlides
    id (主キー)
    title (画像タイトル)
    description (画像説明)
    user_id (外部キー)
    views_count (ビュー数)
    likes_count (ライク数)
    rating (画像の類型)
    created_at (作成日時)
    updated_at (更新日時)
* Images
    id (主キー)
    slide_id (外部キー)
    image_file (画像ファイル)
    created_at (作成日時)
    updated_at (更新日時)
* ImageComments
    id (主キー)
    user_id (外部キー)
    image_id (外部キー)
    content (コメント内容)
    created_at (作成日時)
    updated_at (更新日時)
    parent_comment_id (親コメントのID)
* ImageLikes
    id (主キー)
    user_id (外部キー)
    image_id (外部キー)
    created_at (作成日時)
* Tags
    id (主キー)
    name (タグ名)
    slug (タグのスラッグ)
* Forum
    id (主キー)
    category (フォーラムのカテゴリ)
    title (フォーラムタイトル)
    description (フォーラムの説明)
    is_admin (管理者かどうか)
    threads_count (スレッド数)
    posts_count (投稿数)
    created_at (作成日時)
    updated_at (更新日時)
* ForumThreads
    id (主キー)
    title (スレッドタイトル)
    forum_id (外部キー)
    posts_count (投稿数)
    views_count (ビュー数)
    is_sticky (スティッキーかどうか)
    is_locked (ロックされているかどうか)
    created_at (作成日時)
    updated_at (更新日時)
* ForumPosts
    id (主キー)
    user_id (外部キー)
    thread_id (外部キー)
    content (投稿内容)
    created_at (作成日時)
    updated_at (更新日時)

## API Endpoints (APIのエンドポイント)

* Register
  * Method: POST
    Endpoint: /api/users/register/
    Parameters: username, password, email
    Description: ユーザーを登録します。
    Authentication: なし
* Login
  * Method: POST
    Endpoint: /api/users/login/
    Parameters: username, password
    Description: ログインします。
    Authentication: なし
* Logout
  * Method: POST
    Endpoint: /api/users/logout/
    Parameters: なし
    Description: ログアウトします。
    Authentication: JWTトークン認証が必要
* Profile
  * Method: GET
    Endpoint: /api/profile/{user_name}
    Parameters: なし
    Description: ユーザーのプロフィールを取得します。
    Authentication: なし
* User
  * Method: GET
    Endpoint: /api/users/{user_id}
    Parameters: なし
    Description: ユーザーの情報を取得します。
    Authentication: JWTトークン認証が必要
  * Method: PUT/PATCH
    Endpoint: /api/users/{user_id}
    Parameters: nikename, email, password, avatar, header, description, locale
    Description: ユーザーのプロフィールを更新します。
    Authentication: JWTトークン認証が必要
* Following
  * Method: GET
    Endpoint: /api/users/{user_id}/following
    Parameters: なし
    Description: 指定したユーザーがフォローしているユーザー一覧を取得します。
    Authentication: なし（公開API）
  * Method: POST
    Endpoint: /api/users/following
    Parameters: following_user_id (必須): フォローするユーザーのID
    Description: 指定したユーザーをフォローします。
    Authentication: JWTトークン認証が必要
  * Method: DELETE
    Endpoint: /api/users/following
    Parameters: following_user_id (必須): フォローするユーザーのID
    Description: 指定したフォローを解除します。
    Authentication: JWTトークン認証が必要
* Followers
  * Method: GET
    Endpoint: /api/users/{user_id}/followers
    Parameters: なし
    Description: 指定したユーザーのフォロワー一覧を取得します。
    Authentication: なし（公開API）
* Friends
  * Method: GET
    Endpoint: /api/users/{user_id}/friends
    Parameters: なし
    Description: 指定したユーザーの友達一覧を取得します。
    Authentication: JWTトークン認証が必要
  * Method: POST
    Endpoint: /api/users/{user_id}/friends
    Parameters: friend_user_id (必須): 友達に追加するユーザーのID
    Description: 指定したユーザーを友達に追加します。
    Authentication: JWTトークン認証が必要
  * Method: DELETE
    Endpoint: /api/users/{user_id}/friends
    Parameters: friend_user_id (必須): 友達に追加するユーザーのID
    Description: 指定した友達を削除します。
    Authentication: JWTトークン認証が必要
* Friend Requests
  * Method: GET
    Endpoint: /api/users/{user_id}/friends/requests
    Parameters: なし
    Description: 指定したユーザーが受け取ったフレンドリクエストの一覧を取得します。
    Authentication: JWTトークン認証が必要
  * Method: POST
    Endpoint: /api/users/{user_id}/friends/requests/accept
    Parameters: friend_request_user_id (必須): 友達にリクエストするユーザーのID
    Description: 指定したフレンドリクエストを承認します。
    Authentication: JWTトークン認証が必要
  * Method: POST
    Endpoint: /api/users/{user_id}/friends/requests/reject
    Parameters: friend_request_user_id (必須): 友達にリクエストするユーザーのID
    Description: 指定したフレンドリクエストを拒否します。
    Authentication: JWTトークン認証が必要
  * Method: DELETE
    Endpoint: /api/users/{user_id}/friends/requests/cancel
    Parameters: friend_request_user_id (必須): 友達にリクエストするユーザーのID
    Description: 指定したフレンドリクエストをキャンセルします。
    Authentication: JWTトークン認証が必要
* Videos
  * Method: GET
    Endpoint: /api/videos/
    Parameters: なし
    Description: 動画一覧を取得します。
    Authentication: なし（公開API）
  * Method: POST
    Endpoint: /api/videos/
    Parameters:
      title (必須): 動画タイトル
      description (必須): 動画説明
      video_file (必須): 動画ファイル
      rating (必須): 動画の類型
    Description: 新しい動画をアップロードします。
    Authentication: JWTトークン認証が必要
  * Method: GET
    Endpoint: /api/videos/{video_id}/
    Parameters: なし
    Description: 指定したIDの動画を取得します。
    Authentication: なし（公開API）
  * Method: PUT
    Endpoint: /api/videos/{video_id}/
    Parameters:
      title: 動画タイトル
      description: 動画説明
      video_file: 動画ファイル
      rating: 動画の類型
    Description: 指定したIDの動画を更新します。
    Authentication: JWTトークン認証が必要
  * Method: DELETE
    Endpoint: /api/videos/{video_id}/
    Parameters: なし
    Description: 指定したIDの動画を削除します。
    Authentication: JWTトークン認証が必要
* Tags
  * Method: GET
    Endpoint: /api/tags/
    Parameters: なし
    Description: tag一覧を取得します。
    Authentication: なし（公開API）
  * Method: POST
    Endpoint: /api/tags/
    Parameters:
      name (必須): Tag名
    Description: tagを作成します。
    Authentication: JWTトークン認証が必要
  * Method: DELETE
    Endpoint: /api/tags/
    Parameters: tag (必須): 削除するtagのID (tag name)
    Description: 指定したIDのTagを削除します。
    Authentication: JWTトークン認証が必要
* ImageSlides
  * Method: GET
    Endpoint: /api/images/
    Parameters: なし
    Description: 画像スライド一覧を取得します。
    Authentication: なし（公開API）
  * Method: POST
    Endpoint: /api/images/
    Parameters:
      title (必須): 画像スライドのタイトル
      description (必須): 画像スライドの説明
      rating (必須): 画像スライドの類型
      images[] (必須): アップロードする画像ファイル（複数可）
    Description: 新しい画像スライドを作成します。
    Authentication: JWTトークン認証が必要
  * Method: GET
    Endpoint: /api/images/{id}/
    Parameters:
      id (必須): 取得する画像スライドのID
    Description: 指定した画像スライドを取得します。
    Authentication: なし（公開API）
  * Method: PUT
    Endpoint: /api/images/{id}/
    Parameters:
      id (必須): 更新する画像スライドのID
      title (オプション): 画像スライドのタイトル
      description (オプション): 画像スライドの説明
      rating (オプション): 画像スライドの類型
    Description: 指定した画像スライドを更新します。
    Authentication: JWTトークン認証が必要
  * Method: DELETE
    Endpoint: /api/images/{id}/
    Parameters:
      id (必須): 削除する画像スライドのID
    Description: 指定した画像スライドを削除します。
    Authentication: JWTトークン認証が必要
* Images
  * Method: GET
    Endpoint: /api/images/{slide_id}/image/
    Parameters: なし
    Description: 指定した画像スライドのすべての画像を取得します。
    Authentication: なし（公開API）
  * Method: POST
    Endpoint: /api/images/{slide_id}/image/
    Parameters:
      image_file (必須): アップロードする画像ファイル
    Description: 指定した画像スライドに画像を追加します。
    Authentication: JWTトークン認証が必要
  * Method: GET
    Endpoint: /api/images/{slide_id}/image/{id}/
    Parameters: なし
    Description: 指定した画像を取得します。
    Authentication: なし（公開API）
  * Method: DELETE
    Endpoint: /api/images/{slide_id}/image/{id}/
    Parameters: なし
    Description: 指定した画像を削除します。
    Authentication: JWTトークン認証が必要
* Video Likes
  * Method: GET
    Endpoint: /api/videos/{id}/like/
    Parameters: なし
    Description: 指定した動画にいいねをしたユーザー一覧を取得します。
    Authentication: なし（公開API）
  * Method: POST
    Endpoint: /api/videos/{id}/like/
    Parameters: なし
    Description: 指定した動画にいいねをします。
    Authentication: JWTトークン認証が必要
  * Method: POST
    Endpoint: /api/videos/{id}/unlike/
    Parameters: なし
    Description: 指定した動画のいいねを取り消します。
    Authentication: JWTトークン認証が必要
* ImageSlide Likes
  * Method: GET
    Endpoint: /api/images/{id}/like/
    Parameters: なし
    Description: 指定した画像スライドにいいねをしたユーザー一覧を取得します。
    Authentication: なし（公開API）
  * Method: POST
    Endpoint: /api/images/{id}/like/
    Parameters: なし
    Description: 指定した画像スライドをいいねします。
    Authentication: JWTトークン認証が必要
  * Method: POST
    Endpoint: /api/images/{id}/unlike/
    Parameters: なし
    Description: 指定した画像スライドをのいいねを取り消します。
    Authentication: JWTトークン認証が必要
* Video Comments
  * Method: GET
    Endpoint: /api/videos/{id}/comments/
    Parameters: なし
    Description: 指定した動画のコメント一覧を取得します。
    Authentication: なし（公開API）
  * Method: POST
    Endpoint: /api/videos/{id}/comments/
    Parameters:
      content (必須): コメントの本文
      parent_comment_id (オプション): 親コメントのID
    Description: 指定した動画にコメントを追加します。
    Authentication: JWTトークン認証が必要
  * Method: PUT
    Endpoint: /api/videos/{id}/comments/{comment_id}/
    Parameters: なし
    Description: 指定したコメントを更新します。
    Authentication: JWTトークン認証が必要
  * Method: DELETE
    Endpoint: /api/videos/{id}/comments/{comment_id}/
    Parameters: なし
    Description: 指定したコメントを削除します。
    Authentication: JWTトークン認証が必要
* ImageSlide Comments
  * Method: GET
    Endpoint: /api/images/{id}/comments/
    Parameters: なし
    Description: 指定した画像スライドのコメント一覧を取得します。
    Authentication: なし（公開API）
  * Method: POST
    Endpoint: /api/images/{id}/comments/
    Parameters:
      content (必須): コメントの本文
      parent_comment_id (オプション): 親コメントのID
    Description: 指定した画像スライドにコメントを追加します。
    Authentication: JWTトークン認証が必要
  * Method: PUT
    Endpoint: /api/images/{id}/comments/{comment_id}/
    Parameters: なし
    Description: 指定したコメントを更新します。
    Authentication: JWTトークン認証が必要
  * Method: DELETE
    Endpoint: /api/images/{id}/comments/{comment_id}/
    Parameters: なし
    Description: 指定したコメントを削除します。
    Authentication: JWTトークン認証が必要
* Playlist
  * Method: GET
    Endpoint: /api/playlists/
    Parameters: なし
    Description: プレイリスト一覧を取得します。
    Authentication: なし（公開API）
  * Method: POST
    Endpoint: /api/playlists/
    Parameters: name (必須): プレイリスト名
    Description: 新しいプレイリストを作成します。
    Authentication: JWTトークン認証が必要
  * Method: GET
    Endpoint: /api/playlists/{playlist_id}/
    Parameters: なし
    Description: 指定したプレイリストの詳細を取得します。
    Authentication: なし（公開API）
  * Method: DELETE
    Endpoint: /api/playlists/{playlist_id}/
    Parameters: なし
    Description: 指定したプレイリストを削除します。
    Authentication: JWTトークン認証が必要
  * Method: POST
    Endpoint: /api/playlists/{playlist_id}/{video_id}/
    Parameters: なし
    Description: 指定したプレイリストにビデオを追加します。
    Authentication: JWTトークン認証が必要
  * Method: DELETE
    Endpoint: /api/playlists/{playlist_id}/{video_id}/
    Parameters: なし
    Description: 指定したプレイリストからビデオを削除します。
    Authentication: JWTトークン認証が必要
* Post
  * Method: GET
    Endpoint: /api/posts/
    Parameters: なし
    Description: ポスト一覧を取得します。
    Authentication: なし（公開API）
  * Method: POST
    Endpoint: /api/posts/
    Parameters:
      title (必須): 投稿のタイトル
      content (必須): 投稿の本文
    Description: 新しいポストを作成します。
    Authentication: JWTトークン認証が必要
  * Method: PUT
    Endpoint: /api/posts/{id}/
    Parameters: なし
    Description: 指定したポストを更新します。
    Authentication: JWTトークン認証が必要
  * Method: DELETE
    Endpoint: /api/posts/{id}/
    Parameters: なし
    Description: 指定したポストを削除します。
    Authentication: JWTトークン認証が必要
* PostComments
  * Method: GET
    Endpoint: /api/posts/{id}/comments/
    Parameters: なし
    Description: 指定したポストのコメント一覧を取得します。
    Authentication: なし（公開API）
  * Method: POST
    Endpoint: /api/posts/{id}/comments/
    Parameters:
      content (必須): 投稿の本文
      parent_comment_id (オプション): 親コメントのID
    Description: 指定したポストにコメントを追加します。
    Authentication: JWTトークン認証が必要
  * Method: PUT
    Endpoint: /api/posts/{id}/comments/{comment_id}/
    Parameters: なし
    Description: 指定したコメントを更新します。
    Authentication: JWTトークン認証が必要
  * Method: DELETE
    Endpoint: /api/posts/{id}/comments/{comment_id}/
    Parameters: なし
    Description: 指定したコメントを削除します。
    Authentication: JWTトークン認証が必要
* ProfileComments
  * Method: GET
    Endpoint: /api/profile/{user_id}/comments/
    Parameters: なし
    Description: 指定したユーザーのプロフィールコメント一覧を取得します。
    Authentication: なし（公開API）
  * Method: POST
    Endpoint: /api/profile/{user_id}/comments/
    Parameters:
      content (必須): 投稿の本文
      parent_comment_id (オプション): 親コメントのID
    Description: 指定したユーザーのプロフィールにコメントを追加します。
    Authentication: JWTトークン認証が必要
  * Method: PUT
    Endpoint: /api/profile/{user_id}/comments/{comment_id}/
    Parameters: なし
    Description: 指定したコメントを更新します。
    Authentication: JWTトークン認証が必要
  * Method: DELETE
    Endpoint: /api/profile/{user_id}/comments/{comment_id}/
    Parameters: なし
    Description: 指定したコメントを削除します。
    Authentication: JWTトークン認証が必要
* MessageThreads
  * Method: GET
    Endpoint: /api/message_threads/
    Parameters: なし
    Description: ユーザーのメッセージスレッドの一覧を取得します。
    Authentication: JWTトークン認証が必要
  * Method: POST
    Endpoint: /api/message_threads/
    Parameters: 
      recipient_id (必須): 受信者のID
      title (必須): メッセージスレッドのタイトル
      content (必須): メッセージの内容
    Description: 新しいメッセージスレッドを作成します。
    Authentication: JWTトークン認証が必要
  * Method: DELETE
    Endpoint: /api/message_threads/{thread_id}/
    Parameters: なし
    Description: 指定したメッセージスレッドを削除します。
    Authentication: JWTトークン認証が必要
* Messages
  * Method: GET
    Endpoint: /api/message_threads/{thread_id}/messages/
    Parameters: なし
    Description: 指定したメッセージスレッドのメッセージ一覧を取得します。
    Authentication: JWTトークン認証が必要
  * Method: POST
    Endpoint: /api/message_threads/{thread_id}/messages/
    Parameters: content (必須): メッセージの内容
    Description: 指定したメッセージスレッドにメッセージを送信します。
    Authentication: JWTトークン認証が必要
  * Method: DELETE
    Endpoint: /api/message_threads/{thread_id}/messages/{message_id}/
    Parameters: なし
    Description: 指定したメッセージを削除します。
    Authentication: JWTトークン認証が必要
* Notifications
  * Method: GET
    Endpoint: /api/notifications/
    Parameters: なし
    Description: 通知一覧を取得します。
    Authentication: JWTトークン認証が必要
  * Method: PUT/PATCH
    Endpoint: /api/notifications/{notification_id}/
    Parameters: なし
    Description: 指定した通知の既読状態を更新します。
    Authentication: JWTトークン認証が必要
* NotificationSettings
  * Method: GET
    Endpoint: /api/notification_settings/
    Parameters: なし
    Description: 通知設定を取得します。
    Authentication: JWTトークン認証が必要
  * Method: PUT/PATCH
    Endpoint: /api/notification_settings/
    Parameters:
      mension_enabled (任意): メンション通知の設定値
      comment_enabled (任意): コメント通知の設定値
      reply_enabled (任意): 返信通知の設定値
    Description: 通知設定を更新します。
    Authentication: JWTトークン認証が必要
* Forum
  * Method: GET
    Endpoint: /api/forum/
    Parameters: なし
    Description: フォーラム一覧を取得します。
    Authentication: なし（公開API）
  * Method: POST
    Endpoint: /api/forum/
    Parameters:
      category (必須): フォーラムのカテゴリ
      title (必須): フォーラムタイトル
      description (必須): フォーラムの説明
      is_admin (必須): 管理者かどうか
    Description: 新しいフォーラムを作成します。
    Authentication: 管理者権限が必要、JWTトークン認証が必要
  * Method: DELETE
    Endpoint: /api/forum/{forum_id}/
    Parameters: なし
    Description: 指定したフォーラムを削除します。
    Authentication: 管理者権限が必要、JWTトークン認証が必要
* ForumThreads
  * Method: GET
    Endpoint: /api/forum/{forum_id}/threads/
    Parameters: なし
    Description: 指定したフォーラムのスレッド一覧を取得します。
    Authentication: なし（公開API）
  * Method: POST
    Endpoint: /api/forum/{forum_id}/threads/
    Parameters:
      title (必須): スレッドのタイトル
      content (必須): スレッドの内容
    Description: 指定したフォーラムに新しいスレッドを作成します。
    Authentication: JWTトークン認証が必要
  * Method: PUT
    Endpoint: /api/forum/{forum_id}/threads/{thread_id}/
    Parameters:
      title (必須): スレッドのタイトル
    Description: 指定したスレッドを更新します。
    Authentication: JWTトークン認証が必要
  * Method: DELETE
    Endpoint: /api/forum/{forum_id}/threads/{thread_id}/
    Parameters: なし
    Description: 指定したスレッドを削除します。
    Authentication: JWTトークン認証が必要
* ForumPosts
  * Method: GET
    Endpoint: /api/forum/threads/{thread_id}/posts/
    Parameters: なし
    Description: 指定したスレッドの投稿一覧を取得します。
    Authentication: なし（公開API）
  * Method: POST
    Endpoint: /api/forum/threads/{thread_id}/posts/
    Parameters:
      content (必須): 投稿の内容
    Description: 指定したスレッドに新しい投稿を作成します。
    Authentication: JWTトークン認証が必要
  * Method: PUT
    Endpoint: /api/forum/threads/{thread_id}/posts/{post_id}/
    Parameters:
      content (必須): 投稿の内容
    Description: 指定した投稿を更新します。
    Authentication: JWTトークン認証が必要
  * Method: DELETE
    Endpoint: /api/forum/threads/{thread_id}/posts/{post_id}/
    Parameters: なし
    Description: 指定した投稿を削除します。
    Authentication: JWTトークン認証が必要

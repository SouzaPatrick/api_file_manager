from app import db

class Bucket(db.Model):
    __tablename__ = 'bucket'  # Nome da tabela no banco

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    name = db.Column(db.String(100))
    creation_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    #Relacionamentos
    user = db.relationship("User", back_populates="bucket", lazy="joined")
    files = db.relationship("File", back_populates="bucket", lazy="joined")

    # Representação das consultas no banco, como irão ser apresentadas
    def __repr__(self):
        return "<Bucket %r>" % self.name

class File(db.Model):
    __tablename__ = 'file'  # Nome da tabela no banco

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    name = db.Column(db.String(100))
    path = db.Column(db.String(120))
    size = db.Column(db.String(20))
    extension = db.Column(db.String(5))
    insertion_date = db.Column(db.DateTime)
    expiration_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    bucket_id = db.Column(db.Integer, db.ForeignKey('bucket.id'))

    user = db.relationship("User", back_populates="files", lazy="joined")
    bucket = db.relationship("Bucket", back_populates="files", lazy="joined")

    # Representação das consultas no banco, como irão ser apresentadas
    def __repr__(self):
        return "<File %r>" % self.name

class User(db.Model):
    __tablename__ = "user"  # Nome da tabela no banco

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    username = db.Column(db.String(64))
    usercpf = db.Column(db.String(14), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime, )
    first_seen = db.Column(db.DateTime)
    # profile_id = db.Column(db.Integer, db.ForeignKey("profile.id"))

    # posts = db.relationship("Post", backref="author", lazy="dynamic")
    files = db.relationship("File", back_populates="user", lazy="joined")
    bucket = db.relationship("Bucket", back_populates="user", lazy="joined")

    # followed = db.relationship(
    #     "User",
    #     secondary=followers,
    #     primaryjoin=(followers.c.follower_id == id),
    #     secondaryjoin=(followers.c.followed_id == id),
    #     backref=db.backref("followers", lazy="dynamic"),
    #     lazy="dynamic")

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    # Representação das consultas no banco, como irão ser apresentadas
    def __repr__(self):
        return "<User %r>" % self.username
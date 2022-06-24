package com.example.airboard;

import androidx.annotation.NonNull;
import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;

import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.util.Log;
import android.widget.Toast;

import com.google.android.gms.tasks.OnFailureListener;
import com.google.android.gms.tasks.OnSuccessListener;
import com.google.ar.sceneform.AnchorNode;
import com.google.ar.sceneform.assets.RenderableSource;
import com.google.ar.sceneform.math.Vector3;
import com.google.ar.sceneform.rendering.ModelRenderable;
import com.google.ar.sceneform.ux.ArFragment;
import com.google.firebase.FirebaseApp;
import com.google.firebase.auth.AuthResult;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseUser;
import com.google.firebase.auth.OAuthCredential;
import com.google.firebase.storage.FileDownloadTask;
import com.google.firebase.storage.FirebaseStorage;
import com.google.firebase.storage.StorageReference;

import java.io.File;
import java.io.IOException;
import java.io.FileReader;
import java.lang.Character;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Locale;
import java.util.Map;


public class MainActivity extends AppCompatActivity {

    Vector3 pos; int size = 0;
    FirebaseStorage storage;
    FirebaseAuth mAuth;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        FirebaseApp.initializeApp(this);
        storage = FirebaseStorage.getInstance();


    }

    private void signInAnonymously() {
        mAuth.signInAnonymously().addOnSuccessListener(this, new  OnSuccessListener<AuthResult>() {
            @Override
            public void onSuccess(AuthResult authResult) {
                modelRender();
            }
        })
                .addOnFailureListener(this, new OnFailureListener() {
                    @Override
                    public void onFailure(@NonNull Exception exception) {

                    }
                });
    }


    void modelRender(){

        StorageReference pred_text = storage.getReference().child("predicted_text.txt");


        List<Character> text = new ArrayList<>();
        try {

            File file = File.createTempFile("predicted_text","txt");
            pred_text.getFile(file).addOnSuccessListener(new OnSuccessListener<FileDownloadTask.TaskSnapshot>() {
                @RequiresApi(api = Build.VERSION_CODES.N)
                @Override
                public void onSuccess(FileDownloadTask.TaskSnapshot taskSnapshot) {

                    try{
                        FileReader fr = new FileReader(file);
                        int content; int i=0;
                        while ((content = fr.read()) != -1) {
                            text.add(Character.toLowerCase(((char) content)));
                        }
                        try {
                            System.out.println(text);
                            final Map<Character, File> models = new HashMap<>();
                            for(int l=0;l<text.size();l++)
                            {
                                final int curr = l;
                                File model = File.createTempFile(Character.toString(text.get(l)).toLowerCase(Locale.ROOT)+"_file","glb");
                                storage.getReference().child(Character.toString(text.get(l))+".glb").getFile(model).addOnSuccessListener(new OnSuccessListener<FileDownloadTask.TaskSnapshot>() {
                                    @RequiresApi(api = Build.VERSION_CODES.N)
                                    @Override
                                    public void onSuccess(FileDownloadTask.TaskSnapshot taskSnapshot) {
                                        System.out.println(curr);
                                        models.put(text.get(curr), model);

                                        if (models.size() == text.size())
                                        {
                                            for(int index=0;index<text.size();index++)
                                            {

                                                File model = models.get(text.get(index));
                                                buildModel(model);
                                            }
                                        }


                                    }

                                })
                                ;

                            };

                        } catch (Exception e) {
                            e.printStackTrace();
                        }

                    }catch(Exception e){}
                }
            });
        } catch (Exception e){
            e.printStackTrace();

        }
        ArFragment arFragment = (ArFragment) getSupportFragmentManager()
                .findFragmentById(R.id.arfragment);


        arFragment.setOnTapArPlaneListener((hitResult, plane, motionEvent) -> {
            for (int i = 0; i < text.size(); i++) {
                AnchorNode anchorNode = new AnchorNode(hitResult.createAnchor());
                anchorNode.setRenderable(renderable.removeFirst());
                if (size == 0)
                    pos = anchorNode.getWorldPosition();
                else
                    pos.x += 1000;
                anchorNode.setLocalPosition(pos);
                arFragment.getArSceneView().getScene().addChild(anchorNode);
                pos = anchorNode.getRight();
                size += 1;
            }
        });
    }
    @Override
    protected void onStart() {

        super.onStart();
        mAuth = FirebaseAuth.getInstance();

        FirebaseUser user = mAuth.getCurrentUser();
        if (user != null) {
            modelRender();
        } else {
            signInAnonymously();
        }



    }

    private LinkedList<ModelRenderable> renderable = new LinkedList<ModelRenderable>();

    @RequiresApi(api = Build.VERSION_CODES.N)
    private void buildModel(File file) {


        RenderableSource renderableSource = RenderableSource
                .builder()
                .setSource(this, Uri.parse(file.getPath()), RenderableSource.SourceType.GLB)
                .setRecenterMode(RenderableSource.RecenterMode.ROOT)
                .build();

        ModelRenderable
                .builder()
                .setSource(this,renderableSource )
                .setRegistryId(file.getPath())
                .build()
                .thenAccept(modelRenderable -> {
                    Toast.makeText(this,"Model Built", Toast.LENGTH_SHORT).show();

                    renderable.add(modelRenderable);
                });

    }
}
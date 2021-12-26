<?php

namespace App\Controller;

use App\Entity\User;
use App\Form\UserType;
use Symfony\Bridge\Doctrine\ManagerRegistry;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Component\Security\Core\Validator\Constraints\UserPassword;
use Symfony\Bundle\FrameworkBundle\Controller\Controller;


class HomeController extends AbstractController
{

    #[Route("/", name: "home")]

    public function index($doctrine)
    {
        $users = $this->$doctrine->getRepository(User::class)->findAll();
        return $this->render(view: 'index.html.twig', parameters: [
            'users' => $users,
        ]);
    }

//    /**
//     * @Route("/create", name: "create_user")
//     * @param Request $request
//     * @return Response
//     */
//    public function createUser(Request $request)
//    {
//        $user = new User();
//        $form = $this->createForm(type: UserType::class, options: [$user]);
//        $em = $this->getDoctrine()->getManager();
//        $form->handleRequest($request);
//
//        if (($form->isSubmitted()) && ($form->isValid()))
//        {
//            $em->persist($user);
//            $em->flush();
//            return $this->redirectToRoute(route: "app_home_index");
//        }
//        return $this->render(view: 'index.html.twig', parameters: [
//            'form' => $form,
//        ]);
//    }
}